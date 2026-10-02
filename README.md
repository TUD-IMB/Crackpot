# Crackpot – Concrete Research And Crack Knowledge Photogrammetric Observation Tool

Crackpot extracts crack properties from photographs of cracks. It guides a set
of images through calibration, crack masking, skeleton extraction and export,
and computes crack length, area and mean crack width from a calibrated
resolution. Automated results can be corrected by hand at every stage.

## Installation

Crackpot is installed with `pip` and started with the `crackpot` command:

```
pip install crackpot
crackpot
```

The automatic crack detection is optional, because it requires TensorFlow,
which takes up considerably more space than the application itself. The base
installation therefore only covers the manual annotation workflow, in which the
crack mask is drawn by hand (`None` in the masking stage). If the automatic
detection is unavailable, the corresponding entry in the model dropdown is
greyed out and `None` is preselected.

To install the automatic detection as well, use the `tensorflow` extra:

```
pip install "crackpot[tensorflow]"
```

Both variants can be installed later on: running the second command on an
existing installation adds the missing parts. On Linux and macOS the quotes are
required, otherwise the shell interprets the brackets as a file pattern.

> Installing into a virtual environment is recommended.
> Crackpot requires Python 3.10 or newer; the `tensorflow` extra additionally
> requires a Python version TensorFlow provides a release for.

## Documentation

- The handbook walks through every stage of the workflow:
  [src/crackpot/resources/docs/README.md](https://github.com/TUD-IMB/Crackpot/blob/master/src/crackpot/resources/docs/README.md).
  It is also available offline from within the application, via
  Help → Documentation.
- How the code is organized is described in
  [doc/DevelopmentDocumentation.md](https://github.com/TUD-IMB/Crackpot/blob/master/doc/DevelopmentDocumentation.md),
  which also links to the pages on how the skeleton is cleaned and measured.
- How a new version is built and published on PyPI is described in
  [doc/Packaging.md](https://github.com/TUD-IMB/Crackpot/blob/master/doc/Packaging.md).

## Running from a source checkout

```
pip install -e .
crackpot
```

The Qt interface (`.ui`), the resource collection (`.qrc`) and the translations
(`.ts`) are compiled into Python modules, which are kept in the repository.
After one of them has been changed, the generated modules are refreshed with:

```
python src/convertpyfile.py
```

## License

Crackpot is licensed under the GNU General Public License v3.0 only, see
[LICENSE](https://github.com/TUD-IMB/Crackpot/blob/master/LICENSE).

Two third-party components ship with it under their own terms:

- The user interface icons are taken from
  [Huge Icons](https://icon-sets.iconify.design/hugeicons/) and are licensed
  under the MIT License, see `src/crackpot/resources/license/icon_MIT_LICENSE.txt`.
- The pre-trained detection model is taken from
  [Concrete Crack Segmentation](https://github.com/Subham2901/Concrete_Crack_Segmentation)
  and is licensed under the MIT License, see
  `src/crackpot/resources/license/model_MIT_LICENSE.txt`.
