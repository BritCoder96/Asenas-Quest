﻿# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This extra contains a basic implementation of voice support. Right
# now, voice is given its own toggle, and can either be turned on or
# turned off. In the future, we'll probably provide some way of
# toggling it on or off for individual characters.
#
# To use it, place a voice "<sndfile>" line before each voiced line of
# dialogue.
#
#     voice "e_1001.ogg"
#     e "Voice support lets you add the spoken word to your games."
#
# Normally, a voice is cancelled at the start of the next
# interaction. If you want a voice to span interactions, call
# voice_sustain.
#
#     voice "e_1002.ogg"
#     e "Voice sustain is a technique that allows the same voice file.."
#
#     $ voice_sustain()
#     e "...to play for two lines of dialogue."

init -1500 python:

    _voice = object()
    _voice.play = None
    _voice.sustain = False
    _voice.seen_in_lint = False
    _voice.tag = None

    # The voice filename format. This may contain the voice tag
    
    config.voice_filename_format = "{filename}"

    # Call this to specify the voice file that will be played for
    # the user. This peice only gathers the information so 
    # voice_interact can play the right file.
    def voice(filename, tag=None):
        """
        :doc: voice

        Plays `filename` on the voice channel. The equivalent of the voice
        statement.

        `filename`
            The filename to play. This is used with 
            :var:`config.voice_filename_format` to produce the 
            filename that will be played.
        
        `tag`
            If this is not None, it should be a string giving a 
            voice tag to be played. If None, this takes its
            default value from the voice_tag of the Character 
            that causes the next interaction.

            The voice tag is used to specify which character is 
            speaking, to allow a user to mute or unmute the 
            voices of particular characters.
        """

        if not config.has_voice:
            return

        fn = config.voice_filename_format.format(filename=filename)
        _voice.play = fn
        
    # Call this to specify that the currently playing voice file
    # should be sustained through the current interaction.
    def voice_sustain(ignored="", **kwargs):
        """
        :doc: voice
        
        The equivalent of the voice sustain statement.
        """
        
        if not config.has_voice:
            return
        
        _voice.sustain = True

    # Call this to replay the last bit of voice.
    def voice_replay():
        """
        :doc: voice
        
        Replays the current voice, if possible.
        """
        
        if _last_voice_play is not None:
            renpy.sound.play(_last_voice_play, channel="voice")

    # Returns true if we can replay the voice.
    def voice_can_replay():
        """
        :doc: voice
        
        Returns true if it's possible to replay the current voice.
        """
        
        return _last_voice_play is not None

    class SetVoiceMute(Action):
        """
        :doc: voice_action
        
        If `mute` is true, mutes voices that are played with the given
        `voice_tag`. If `mute` is false, unmutes voices that are played 
        with `voice_tag`.
        """
        
        def __init__(self, voice_tag, mute):
            self.voice_tag = voice_tag
            self.mute = mute
            
        def get_selected(self):
            if self.mute:
                return self.voice_tag in persistent._voice_mute
            else:
                return self.voice_tag not in persistent._voice_mute
        
        def __call__(self):
            if self.mute:
                persistent._voice_mute.add(self.voice_tag)
            else:
                persistent._voice_mute.discard(self.voice_tag)
                
            renpy.restart_interaction()
            
    class ToggleVoiceMute(Action):
        """
        :doc: voice_action
        
        Toggles the muting of `voice_tag`. This is selected if 
        the given voice tag is muted, unless `invert` is true,
        in which case it's selected if the voice is unmuted.
        """
        
        def __init__(self, voice_tag, invert=False):
            self.voice_tag = voice_tag
            self.invert = invert
            
            
        def get_selected(self):
            rv = self.voice_tag in persistent._voice_mute
            
            if self.invert:
                return not rv
            else:
                return rv
        
        def __call__(self):
            if self.voice_tag not in persistent._voice_mute:
                persistent._voice_mute.add(self.voice_tag)
            else:
                persistent._voice_mute.discard(self.voice_tag)
                
            renpy.restart_interaction()

    class VoiceReplay(Action):
        """
        :doc: voice_action
        
        Replays the most recently played voice.
        """
        
        def __call__(self):
            voice_replay()
            
        def get_sensitive(self):
            return voice_can_replay()


init -1500 python hide:

    # basics: True if the game will have voice.
    config.has_voice = True
    
    # The set of voice tags that are currently muted.
    if persistent._voice_mute is None:
        persistent._voice_mute = set()

    # This is called on each interaction, to ensure that the
    # appropriate voice file is played for the user.        
    def voice_interact():
        
        if not config.has_voice:
            return

        if _voice.tag in persistent._voice_mute:
            renpy.sound.stop(channel="voice")
            store._last_voice_play = _voice.play        
        elif _voice.play and not config.skipping:
            renpy.sound.play(_voice.play, channel="voice")
            store._last_voice_play = _voice.play        
        elif not _voice.sustain:
            renpy.sound.stop(channel="voice")
            store._last_voice_play = _voice.play        

        _voice.play = None
        _voice.sustain = False
    
    config.start_interact_callbacks.append(voice_interact)
    config.say_sustain_callbacks.append(voice_sustain)

    def voice_afm_callback():
        return not renpy.sound.is_playing(channel="voice")

    config.afm_callback = voice_afm_callback

    def voice_tag_callback(voice_tag):
        _voice.tag = voice_tag
        
    config.voice_tag_callback = voice_tag_callback

python early hide:

    def parse_voice(l):
        fn = l.simple_expression()
        if fn is None:
            renpy.error('expected simple expression (string)')

        if not l.eol():
            renpy.error('expected end of line')

        return fn

    def execute_voice(fn):
        fn = eval(fn)
        voice(fn)

    def lint_voice(fn):
        _voice.seen_in_lint = True

        fn = _try_eval(fn, 'voice filename')
        if not isinstance(fn, basestring):
            return
            
        fn = config.voice_filename_format.format(filename=fn)
            
        if not renpy.loadable(fn):
            renpy.error('voice file %r is not loadable' % fn)

    renpy.statements.register('voice',
                              parse=parse_voice,
                              execute=execute_voice,
                              lint=lint_voice,
                              translatable=True)

    def parse_voice_sustain(l):
        if not l.eol():
            renpy.error('expected end of line')

        return None

    def execute_voice_sustain(parsed):
        voice_sustain()

    renpy.statements.register('voice sustain',
                              parse=parse_voice_sustain,
                              execute=execute_voice_sustain,
                              translatable=True)


