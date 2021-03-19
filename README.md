# Cheatsheet

## Project structure
Feel free to change the project tree structure to suit the need.
* core: import implementations of an app like data modelling.
* resources: implementations of the API endpoints
* strings: the different strings for different lanaguages
* libs: support tools, libaries, i.e. data processing, string processing

## Docker
Install Docker and run the following command. You should be able to see the Hello page render
at http://localhost:5000


    $ docker-compose up

To run Pytest and Flake 8:

    $ docker-compose run app sh -c "pytest && flake8"

To run a specific command on Docker:

    $ docker-compose run app sh -c "{command to run}"

To bring everything down:

    $ docker-compose down

For more instructions on how to use and config Docker:
https://docs.docker.com/

## Continous Integration

* .travis.yml: Setting for Travis-CI, which is used for testing and automatic deployment
This Github repository is liked to Travis-CI to run test and coding style

## Style. 
I have read everyone's code and it seems that everyone follow pep8 style. 
