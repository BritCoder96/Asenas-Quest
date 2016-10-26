﻿# You can place the script of your game in this file.
init:
    $ import level_1
    $ import level_2,level_3
    

# Declare images below this line, using the image statement.
image Asena suprised  = "Asena Human Surprised.png"
image Asena happy = "Asena Human Happy.png"
image Asena wolf neutral = "Asena Neutral.png"
image Asena wolf angry = "Asena Angry.png"
image Asena wolf happy = "Asena Happy.png"
image Asena wolf suprised = "Asena Surprised.png"
image Wizard cloaked = "Wizard.png"
image Navi = "Fairy.png" #fuckthishshit
image Forest = "Forest BG.jpg"
image castle = "Castle BG.jpg"
image black = "Black.jpg"
image yolo = "Amulet.png"
# Declare characters used by this game.
define a = Character("Asena", color = "FFBACA")
define f = Character("Ellie", color = "FFBACA") 
define w = Character("Wizard", color = "FFBACA") 
define u = Character("???" , color = "FFBACA") 


define flash = Fade(0.1, 0.0, 0.5, color="#fff")

# The game starts here.
label start:
    scene Forest 
    show Asena happy
    with dissolve 
    
    play sound "birds.mp3"
    play music "forest.mp3"
    
    a "The weather sure is nice today. "
    a "I've never seen so many animals in this part of the woods."
    a "Maybe I can bring a few of 'em home for dinner."
    a "Woah! Is that a wolf over there?!"
    a "He would fetch a good price at the market." 
    a "Steady... Aim..."
    
    scene black 
    with vpunch
    play sound "PUNCH.wav"
    "...."
    "...."
    scene Forest
    with dissolve 
    show Asena suprised at right
    with dissolve 
    a "Huh?"
    a "Ugh, my head is killing me...."
    a "Where am I?" 
    u "You have been brought here by the will of the Guardian of this forest."
    a "Who, me?"
    u "Yes you."
    a "... Who are you?"
    show Asena suprised at right 
    with dissolve 
    show Navi at  top
    with dissolve
    f "I am Ellie, fairy servant to the Guardian of the forest." 
    a "There's no such thing as a fairy. I've been hunting in these woods for years, and I have never encountered a fairy. Not even once!"
    show Navi at top
    with dissolve
    f "We have been watching you, hunter, and you have killed many of the creatures in this forest. You must pay for your sins." #GET OFF MY LAWN
    show Asena suprised at right 
    with dissolve 
    a"What do you mean by repay?!?!"
    a"What are you going to do to me?!?"
    show Navi at top 
    with dissolve 
    f"You shall become the animal of your last kill, and live among the animals until you die!"
    a"You can't do that!"
    stop music fadeout 1
    hide Asena surprised
    play sound "smoke.mp3"
    with flash
    show Asena wolf neutral at right
    with dissolve 
    "..."
    a "What happened?"
    show Asena wolf suprised at right
    with dissolve
    "..."
    "..."
    play music "Zelda - Twilight Princess Music - Menu File Select Screen - www.facebook.comgamemusicSTAR.mp3"
    a"Paws...?"
    a "Wait... AM I A WOLF??" #HASHTAGS ERRYDAY
    show Navi at top
    with dissolve
    f "Can't say I didn't warn you."
    a "This is terrible! How will I support my family now...."
    f "You seem to have a good intention for preying on the creatures of the forest... Maybe you can help me..." #mabeyswag
    show Asena wolf angry at right
    with dissolve
    a"Why would I help you?!?!"
    show yolo at left
    with dissolve 
    f "I will cut you a deal. See this amulet? You humans have been dropping these things everywhere, and they are corrupting my forest. My animals have nowhere to go, and they are trapped here."
    f"You help me, and I'll help you. Go and collect these vile things, and bring them back to me, and I will free you."
    f"Deal?"
    
    menu:
        "Deal.":
            jump deal
              
        "No deal.":
            jump yolo
            
            label deal:
                    show Asena wolf neutral at right
                    a "Fine I will do it."
                    show Navi
                    stop music fadeout 1
                    f "You have chosen well, good luck."
                    jump cc1
            label yolo:
                show Navi
                f "Oh, well. Looks like you'll die a wolf."
                jump end
        
    label cc1:
        scene castle
        play music "castle.mp3"
        hide Navi
        show Asena wolf suprised at right
        with dissolve 
        a "Oof! Where are you taking me? Hey, what's a castle doing here in the middle of the forest?"
        show Navi at top
        with dissolve
        f "There's a dark energy emanating from it. We should investigate."
        with dissolve
        "Use W to jump, A to move left, and D to move right. Use S to pick up the key and enter the door. Bring the key to the door and enter to advance."
        with dissolve
        jump cc
    label cc:
        $ l1_complete = level_1.main()
        if l1_complete == False:
            jump urbad
        elif l1_complete == True:
            jump another
    label urbad:
        menu:
            "Try Again?":
                jump cc1
            "Quit.":
                jump end
    label another:
        show Asena wolf neutral at right
        with dissolve
        a "There are cursed amulets all over this place!"
        u "Who are you? How did you find this place?"
        show Asena wolf angry at right 
        with dissolve
        a "I'm Asena, and this is a fairy of the Guardian of the forest. And who might you be?"
        show Wizard cloaked at left
        with dissolve
        w "Why, I'm the owner of this property, and I request that you leave immediately!"
        f "Not until you tell us where all these amulets came from!"
        w "I've already locked all of the doors. You'll never get in! Take the path of least resistance and begone!"
        hide Wizard cloaked 
        with dissolve 
        show Asena wolf angry at right
        with dissolve
        f "Quick! Find the key to the door!"
        jump cc2
    label cc2:
        $ l2_complete = level_2.main()
        if l2_complete == True:
            jump cc3
        elif l2_complete == False:
            jump retry45
    label retry45:
        menu:
            "Try Again?":
                jump cc2
            "Quit.":
                jump end
    label cc3:
        show Navi at top 
        with dissolve 
        show Asena wolf happy at right
        with dissolve
        a "We're through!"
        f "There are more doors on the other side!"
        f "Which one do we go through? Maybe the wizard left a hint somewhere..."
        menu:
                "The Charred Door":
                    "You fell into a pit of lava and burned..."
                    jump retry
                "The Golden Door":
                    "The door closes behind you and you sense the walls closing in..."
                    jump retry
                "The Open Door":
                    "You proceed onward, hoping that this door is the right door..."
                    jump next 
        label retry:
            menu:
                "Try Again?":
                    jump cc3
                "Quit.":
                    jump end
        label next:
            $ l3_complete = level_3.main()
            if l3_complete == True:
                jump cc4
            elif l3_complete == False:
                jump retry
        label cc4:
            show Navi at top
            with dissolve
            show Asena wolf happy at right
            with dissolve
            f "We're here!"
            show Asena wolf angry at right 
            with dissolve 
            a "Come out and face us, wizard!"
            show Wizard cloaked at left
            with dissolve 
            w "It looks like I have no choice..."
            w "It's time for me to take my leave."
            a "Wait! Come back here!"
            w "Oh I will, soon. You'll die defending this forest."
            hide Wizard cloaked
            play sound "smoke.mp3"
            with flash 
            f "Well, looks like he's gone, for now, at least. We owe you our lives for saving the forest from complete annihilation."
            show Asena wolf happy at right 
            with dissolve 
            a "Huh? Oh yeah, I guess it was nice saving the forest and all that... but... *ahem*" 
            f "Oh right."
            with dissolve
            hide Asena wolf happy
            play sound "smoke.mp3"
            with  flash
            show Asena happy at right
            f "I have lifted the curse from you. You've done well, and you have our thanks for that."
            with dissolve 
            a "I guess we'll see each other around."
            f "Farewell."
            hide Navi 
            show Asena happy
            with dissolve 
            a "See ya! I promise I'll never hurt another animal in your forest again! (Except maybe if I'm reeaaally starving!)"
            "-End"
            "Pygame programming by: Bryan Benson"
            "Ren'Py programming by: David Jadric and Andrew Xu"
            "Art by: Brittany Wendzel"
            
            jump end
    label end:
        return
    return
    
