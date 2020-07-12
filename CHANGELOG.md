# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2020-07-12

### Added

- Added a changelog
- Added some automated testing using Github actions

### Changed

- Switched to Semver - 0.4.0 didn't change the API, just the versioning scheme.

## [0.3] - 2020-07-12

### Added

- YAML and TOML included as output options if the relevant libraries are installed
- Untested support for RFC 7630 hashes (SHA-2 224, 256, 384 and 512)

### Changed

- Switched the default username to 'librenms'

### Fixed

- Method binding issue preventing use of md5
- Kdf was hard coded to sha1

## [0.2] - 2017-04-13

### Fixed

- Confusion between authPriv, authpriv, auth, priv and none
