# Publishing on PyPI

This page describes how a new version of Crackpot is published on [PyPI](https://pypi.org),
so that it can be installed with `pip install crackpot`.

The commands are for Windows and work in the Command Prompt as well as in PowerShell.
They are run from the repository folder and need Python and Git; if `py` is not found, use `python` instead.
The first release on PyPI is version 2.0, which the commands use; for a later release, replace it with the new
number everywhere.

# One-Time Setup

1. Create an account at <https://pypi.org/account/register/> and confirm the e-mail address.
   The account that makes the first upload becomes the owner of the project.
2. Set up two-factor authentication under *Account settings*.
   PyPI requires it for every upload. Keep the recovery codes in a safe place.
3. Create an API token under *Account settings → API tokens → Add API token*
   with the scope *Entire account (all projects)*.
   A token for the project alone is not possible yet, because the project is only created by the first upload.
   The token starts with `pypi-` and is shown only once, so copy it completely and keep it safe.

## Providing the Token

twine, the upload tool, gets the token in one of two ways.

**Entering it at every upload:** nothing has to be prepared, twine asks for the token during the upload (step 3).
This is the better choice on a computer that other people use as well.

**Storing it in `.pypirc`:** twine reads the token from the file `.pypirc` in the user folder and does not ask.
Open the file with Notepad, from the Command Prompt:

```
notepad "%USERPROFILE%\.pypirc"
```

or from PowerShell:

```
notepad "$env:USERPROFILE\.pypirc"
```

Confirm that the file should be created, paste the following section with the complete token, and save:

```ini
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...
```

`username` is literally `__token__`, not the name of the account.
Do not create the file in the Explorer, which saves it as `.pypirc.txt` with the extension hidden.
If the file already exists, add the section to it; if it contains an `index-servers` list, `pypi` must be in it.
The token is stored in plain text, so the file must never be committed or passed on.

# Release Steps

## 1. Set the Version

Start from an up-to-date `master` without uncommitted changes, because the build packs the folder as it is:

```
git switch master
git pull
git status
```

Set the version number and the day of the upload in `src/crackpot/version.py`:

```python
__version__ = "2.0"
RELEASE_DATE = "2026-10-01"
```

Commit and push the change:

```
git commit -m "Set the version to 2.0" src\crackpot\version.py
git push origin master
```

A version number can only be uploaded once, even if the release is deleted later.
Everything in step 2 therefore has to work before the upload.

## 2. Build and Test

```
py -m pip install --upgrade build twine
py -m build --wheel
py -m twine check dist\crackpot-2.0-py3-none-any.whl
```

The first command installs the tools, or updates them (older versions of twine reject the metadata of current builds).
The second creates the wheel `dist\crackpot-2.0-py3-none-any.whl` of about 80 MB, the only file that is published.
The third must report `PASSED`.

Then install the wheel into a new virtual environment and start the application:

```
py -m venv --clear ..\crackpot-test
..\crackpot-test\Scripts\python.exe -m pip install "dist\crackpot-2.0-py3-none-any.whl[tensorflow]"
..\crackpot-test\Scripts\crackpot.exe
```

The About dialog must show the new version, and the automatic detection must be selectable in the masking stage.
If the installation stops with `No matching distribution found for tensorflow`, the Python version is too new for
TensorFlow; create the environment with an older one, for example `py -3.12 -m venv --clear ..\crackpot-test`.

## 3. Upload

```
py -m twine upload dist\crackpot-2.0-py3-none-any.whl
```

With `.pypirc`, twine takes the token from the file.
Without it, twine first warns `This environment is not supported for trusted publishing`, which can be ignored,
and then asks for the token: paste it with a right-click and press Enter; the input stays invisible.
Ctrl+V does not work in this prompt on Windows.
The first upload creates the project at <https://pypi.org/project/crackpot/>.

If the upload fails:

- **`403 Forbidden`**: the token was not accepted, because it is incomplete or belongs to another project.
- **`400 File already exists`**: this version has been uploaded before. Raise the number and start again at step 1.
- **`503`** or **`Connection broken`** after about a minute: the connection is too slow for the 80 MB.
  Upload from a faster one (at 2.4 MB/s it takes about 40 seconds).
  A failed upload does not use up the version number.

## 4. Check the Release

Install the published version the way users do:

```
py -m venv --clear ..\crackpot-test
..\crackpot-test\Scripts\python.exe -m pip install "crackpot[tensorflow]==2.0"
..\crackpot-test\Scripts\crackpot.exe
```

If pip reports `No matching distribution found`, PyPI does not list the new version yet; try again a few minutes later.

## 5. Tag the Release

```
git tag -a v2.0 -m "Release 2.0"
git push origin v2.0
```

The tag records which commit the version was built from.
Set it before pulling or committing anything else, so that it marks the version commit from step 1.

# After the First Release

Replace the account-wide token with one for this project only:
under *Account settings → API tokens*, create a token with the scope *Project: crackpot*,
put it into `.pypirc` in place of the old one if the file is used, and remove the old token on the same page.
Later releases repeat the release steps with a new number.
