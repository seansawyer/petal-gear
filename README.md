# Petal Gear

## Development

### Prerequisites

You will need to install:

- [pyenv](https://github.com/pyenv/pyenv#installation)
- [Pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv).

On Arch Linux, the easiest way to do this is:

```
pacman -Sy pyenv python-pipenv
```

On MacOS, the easiest way to do so is:

```
brew update && brew install pyenv pipenv
```

There are other ways to install both, depending on your preference or circumstance.
Refer to the documentation for more details.

Once you have pyenv installed, you will need to install the target Python version.

```
pyenv install 3.8.6
```


### Setup

Clone the project and set its local Python version.

```
git clone && cd petal-gear
pyenv local 3.8.6
python --version
```

Optional - Exit the project directory and note that your Python version reverts to the global pyenv version.
Then re-enter the project directory and note that it changes back automatically.

```
cd ..
python --version
cd petal-gear
python --version
```

Now you can install the project's dependencies.

```
pipenv install
```

Pipenv will have created a virtual environment for you (if one did not already exist)
and installed the dependencies there.

Once that's done, you should be able to use Pipenv to run the game from the virtualenv.

```
pipenv run python petalgear.py
```

Or, if you like, Pipenv can start a shell for you in the virtualenv, and you can run the
game directly.

```
pipenv shell
python petalgear.py
```


### Development-Only Dependencies

You can also install the development dependencies, although at the moment these are only
relevant to Spacemacs Python layer integration.

```
pipenv install --dev
```

If you use Spacemacs, you'll want to drop a _.venv_ file in the project root.
This enables Spacemacs' Python layer to find the virtualenv in which your libraries and
tools are installed.

```
pipenv --venv > .venv
```
