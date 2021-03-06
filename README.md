# Zilliqa Nano S App 
  
Zilliqa wallet application for Nano S.

## Build

These instructions have been tried on Ubuntu 18.04. Other Linux based platforms may work too.

### Ledger Setup
  - Setup your Ledger Nano S as described in the [official guide](https://support.ledger.com/hc/en-us/articles/360000613793)
  - Update the firmware on your device following the instructions [here](https://support.ledger.com/hc/en-us/articles/360002731113-Update-device-firmware)
    This app has been tested with firmware version `1.6.0`.
  - If you are on Linux, make sure to set the `udev` rules for ledger. Help for it is provided [here](https://support.ledger.com/hc/en-us/articles/115005165269-Fix-connection-issues).
  - You should now be able to use the Ledger Live app and manage your device using it.

### Build Environment
For the sake of this setup, let us have a directory `$LEDGER_DIR` that contains the entire setup. Set this variable to an actual directory you prefer as `export LEDGER_DIR=/home/user/ledger`.

Install platform packages

  - `$sudo apt-get install libudev-dev libusb-1.0-0-dev python3-dev python3-venv gcc-multilib g++-multilib clang pkg-config autoconf libtool libsecp256k1-dev`

Setup a virtual python environment for the ledger libraries. For commands shown below, the presence of `(ledgerenv) ...` indicates that the command is being run in the virtual environment.

  - `$python3 -m venv ${LEDGER_DIR}/ledgerenv`
  - `$source ${LEDGER_DIR}/ledgerenv/bin/activate`
  - (ledgerenv) ... `$pip install ledgerblue`
  - (ledgerenv) ... `$pip install wheel`
  - (ledgerenv) ... `$SECP_BUNDLED_EXPERIMENTAL=1 pip --no-cache-dir install --no-binary secp256k1 secp256k1`

Get Ledger toolchain related pre-requisites

  - `$cd $LEDGER_DIR; git clone https://github.com/LedgerHQ/nanos-secure-sdk`

  - `$wget https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q1-update/+download/gcc-arm-none-eabi-5_3-2016q1-20160330-linux.tar.bz2`
  - `$mkdir devenv; tar -xvjf gcc-arm-none-eabi-5_3-2016q1-20160330-linux.tar.bz2 --directory devenv`

Setup environment for building the app
  - `$export BOLOS_SDK=${LEDGER_DIR}/nanos-secure-sdk/`
  - `$export GCCPATH=${LEDGER_DIR}/devenv/gcc-arm-none-eabi-5_3-2016q1/bin/`

### Build and install

Fetch the sources and build the Zilliqa Ledger Nano-S app. You should find `app.hex` in the `bin/` directory.
  - (ledgerenv) ...`$cd $LEDGER_DIR; git clone https://github.com/Zilliqa/ledger-app-zilliqa`
  - (ledgerenv) ...`export SCRIPT_LD=${LEDGER_DIR}/ledger-app-zilliqa/script.ld`
  - (ledgerenv) ...`$cd ledger-app-zilliqa`
  - (ledgerenv) ...`$make clean; make`

Install the app on your device:
  - (ledgerenv) ...`$make load`

Remove the app from  your device:
  - (ledgerenv) ...`$make delete`

The environment variable `DBG=1` can be provided to `make` to enable debug builds. This will enable printing of debugging messages through `PRINTF` when the [debug firmware](https://ledger.readthedocs.io/en/latest/userspace/debugging.html) is installed. This will also enable checks on [stack overflow](https://ledger.readthedocs.io/en/latest/userspace/troubleshooting.html#stack-overflows).

To ease setting up the environment for everyday development, we suggest having the following script `env.sh`. Edit it as necessary.

```bash
export LEDGER_DIR=/home/user/ledger # edit this as necessary.
export GCCPATH=${LEDGER_DIR}/devenv/gcc-arm-none-eabi-5_3-2016q1/bin/
export BOLOS_SDK=${LEDGER_DIR}/nanos-secure-sdk/
# We use a custom script.ld. So $SCRIPT_LD must be set to point to it.
export SCRIPT_LD=${LEDGER_DIR}/ledger-app-zilliqa/script.ld
source ${LEDGER_DIR}/ledgerenv/bin/activate # activate python3 virtualenv
```

On each of your development shell, just run the following command to setup the environment

  - `$source env.sh`

#### References
  - https://github.com/LedgerHQ/blue-loader-python
  - https://ledger.readthedocs.io/en/latest/userspace/getting_started.html

## JavaScript Interface
Located [here](https://github.com/CryptoAeon/zil-ledger-js-interface)

## Node CLI App
Located [here](https://github.com/CryptoAeon/zil-ledger-node-app)

## Python Test Utils

For each of the commands below, make sure that the virtual python environment is setup, by running the below command in your shell apriori.
  - `source ${LEDGER_DIR}/ledgerenv/bin/activate`

Get public key for index 0
  - (ledgerenv)...`$python getPublicKey.py --index 0`

Get address for index 0
  - (ledgerenv)...`$python getPublicKey.py --index 0 --dispAddr`

Sign a hash from index 0
  - (ledgerenv)...`$python signHash.py --mhash 02E681C8EB3602CDB9261F407E2C2EE6CB9BA996AAA895677E133C02BEFC1F8482 --index 0`

Delete the Zilliqa app
  - (ledgerenv)...`$python -m ledgerblue.deleteApp --targetId 0x31100004 --appName Zilliqa`
  - Alternatively, just run `make delete`

Install `app.hex` to the device
  - (ledgerenv)...`$python -m ledgerblue.loadApp --path "44'/313'"  --curve "secp256k1" --tlv --targetId "0x31100004" --delete --fileName "app.hex" --appName "Zilliqa" --appVersion "0.4.0" --appFlags "0x40"`
  - Alternatively, just run `make load`
