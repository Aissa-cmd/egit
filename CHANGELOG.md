# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] - 2024-11-17

### Changes

- Removed custom handling for `-h/--help` option, now using `argparse` default
- Print usage when called with no args (previously was priting help)

### Fixed

- Fixed error when no git repository is found

## [0.1.3] - 2024-11-17

### Added

- Added check for TODO comments for pre-commit hook
- Added `-V/--version` option

## [0.1.2] - 2024-11-16

### Added

- Initial release
