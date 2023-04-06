import setuptools

setuptools.setup(
    name = 'ks2ool',
    version = '0.0.1',
    author = 'RaisoLiu',
    author_email = 'raisoliu@gmail.com',
    description = 'Tools for analyzing Kilosort2 & phy results.',
    packages = setuptools.find_packages(),
    classifiers = [
    ],
    install_requires = [
        "numpy",
        "tqdm",
        "h5py",
        "scipy",
        "phy",
        "phylib",
    ],
    python_requires = ">=3.7",

)