# GlitchUP
A Python based glitch art generator with visualization.

## Features
- Generate glitch art with random parameters
- Visualize the glitch being applied using websocket technology
- Save the glitch as a png image
- User-friendly interface using a website

## Installation
- Clone the repository
- Install dependencies: `pip install -r dev-requirements.txt`
- (windows) enable WSL
- (windows) download linux distribution from the windows store and install it
- Install redis server using the linux BASH terminal:
    ```bash
    sudo apt-add-repository ppa:redislabs/redis
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install redis-server
    ```
- Restart the redis server: `sudo service redis-server restart`

## Usage
- Run the server: `python src/glitchup/`
- Open the website: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Use the website to generate glitch art
- Profit!

## Authors
- [Binds](https://github.com/akabinds)
- [Brett Fragel](https://github.com/BFragel44)
- [Grace Zhang](https://github.com/Today100)
- [Alec Hitchiner](https://github.com/supereater14)
- [Christopher James](https://github.com/gamingbuddhist)
