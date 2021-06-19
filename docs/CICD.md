# Continous Integration / Continous Deployment

Steps to setup:

1. SET ENV VARIABLES ON GIT HOST (GITHUB,GITLAB)
2. SETUP COVERAGE AND MAINTAIBILITY
3. CHECK WORFLOWS:
   >env:
   >   USING_COVERAGE: "3.10"


## Worflow locally

https://github.com/nektos/act

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```bash
brew install act
```

```bash
act push -v -j codecov-job
```