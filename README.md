---

## Installation

- Clone this repo to your local machine using `https://github.com/Olamyy/ayo_olopon/`

### Setup

- If you want more syntax highlighting, format your code like this:

- Set up a virtual environment and activate it.

- Install required packages
```
pip install -r requirements.txt
```

---

## Playing 

Note the following:

PIM: Penalize Invalid Move || ``boolean``

PITS : Number of pits on a board || ``int``

STONES: Number of stones in a pit || ``int``

GAME TYPE : 

             hvh : Human vs Human
             hvc : Human vs Computer
             cvc : Computer vs Computer


The entry point of the game is the `ayo/cli.py` file.
It initialises the game by:
1. Setting up configuration. 

This can be done in two ways. 

    1. You can either pass your config as a yaml file with the structure below.
       
        pim :     [true|false]
        pits :    [pit_number]
        stones :  [stone_value]
        game:     [hvh | hvc | cvc]
    
    2. Manually call pass the required config variables as a single command while launching the game. 
    
```bash
   python ayo/cli.py --game=hvc --pim=1 --pits=5 --stones=10
   ```

Note: The only really required setup variable is the game type, i.e --game flag

2. Validates the configuration and sets up storage for the game.

3. If the game involves an agent(i.e a computer player), it generates a random name for the agent. If it only involves human players, it prompts for names.
---

## Contributing

> To get started...

### Step 1

- **Option 1**
    - 🍴 Fork this repo!

- **Option 2**
    - 👯 Clone this repo to your local machine using `https://github.com/Olamyy/ayo_olopon/`

### Step 2

- **HACK AWAY!** 🔨🔨🔨

### Step 3

- 🔃 Create a new pull request using <a href="https://github.com/Olamyy/ayo_olopon/compare/" target="_blank">`https://github.com/Olamyy/ayo_olopon/compare/`</a>.