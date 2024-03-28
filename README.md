# Brain Tumor Detection Project

## I. Set up and workflow

### 1. Set up project in your local machine 

Clone the repo

```
git clone https://github.com/harveyphm/brain-tumor-detection
```

Create a desinated branch that your team will work on
```
git checkout -b <your-branch-name>
```

Install GitHub CLI for future pull request. 
[GitHub CLI](https://github.com/cli/cli#installation)

### 2. Before you start working (everytime!)

Make sure your local directory is up-to-date:
```
git checkout main
git pull
git checkout <your-branch-name>
```

### 3. Work on your designated branch

After you done working, you can freely commit code to your designated branch. 
First, ensure you are on your designated branch:
```
git checkout <your-branch-name>
```
or 
```
git branch -a
```
to see which branch you are at.

To add specific files:

```bash
git add path/to/your-file
```

To add all changes at once:
```
git add * 
```

Commit your changes with a message describing what you've done.
```
git commit -m "Your detailed commit message"
```
Push new changes to your designated branch
```
git push -u origin <your-branch-name>
```

### 3. Merge to main branch
When you ready to publish your group work to the rest of the team, you can create a pull request to merge your branch with the main branch

```
gh pr create --base main --head <your-branch-name>
```



