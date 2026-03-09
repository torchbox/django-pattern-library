---
name: upgrading-stylelint
description: Upgrades a project’s Stylelint version or configuration
license: MIT
---

## Overview

Comprehensive project and dependencies review to identify needed changes to upgrade this project to a new Stylelint version, including stylesheet code changes, and potential opt-in improvements based on any changes in the Stylelint release.

## Methodology

### Goals

- Upgrade the project to the target Stylelint release, including any needed dependencies upgrades.
- Baseline QA that the upgrade works correctly - linting passes, test suite passes, all with no deprecation warnings if possible.
- A thorough upgrade report for the user (upgrade methodology, what changed, what further tests to do, links to relevant information), ideally with guidance on opt-in changes to consider.

### Guardrails

- Prefer minimal, reviewable changes. Avoid introducing technical debt.
- Make dependency updates explicit and reproducible (lockfile updates included).
- No fixes unrelated to the upgrade, unless required for the QA checks to pass.
- If a change is ambiguous, choose the option with the least technical debt. Ask for further input if needed.
- When there are issues that seem like bugs in the dependencies, encourage the user to report back with feedback for maintainers.

### Input

To detect from the context or request from the user if unclear:

- Agent mode: whether we want to provide an audit of the needed work for an upgrade, or actually directly do the upgrade. Default: assume "direct update on current code".
- Current versions of Node, Stylelint. Default: read from project configuration (`node --version`, `npm info . devDependencies`)
- Current versions of any Stylelint-related packages, like shared configurations. Default: read from project configuration (`npm info . devDependencies`)
- Target version for Stylelint. Default: assume "latest", fetch the [CHANGELOG](https://raw.githubusercontent.com/stylelint/stylelint/refs/heads/main/CHANGELOG.md) and check which version is latest based on the current date.
- How to run styles linting. Default: read from project documentation or output of task runner like `npm run`.
- Location of the project’s Stylelint config. Default: look for files containing "stylelint" in root directory.

### Reference data sources

Always fetch latest information from the official Stylelint docs and any package docs if possible.

- [Official CHANGELOG](https://raw.githubusercontent.com/stylelint/stylelint/refs/heads/main/CHANGELOG.md)
- Example: [Stylelint 17 migration guide (Markdown source)](https://raw.githubusercontent.com/stylelint/stylelint/refs/heads/main/docs/migration-guide/to-17.md)
- Example: [Stylelint 17 migration guide (web page)](https://stylelint.io/migration-guide/to-17)

Combine it with project-specific information:

- Guidance for contributors in `CONTRIBUTING.md` or other docs.
- Upgrade considerations / test plans / documentation on customizations.

### Reporting

Upgrades are sensitive tasks, it’s critical to provide clear information to the user throughout the upgrade tasks, with clear requests for any extra input. And as a comprehensive report at the end.

- Use text formatting if supported (tables, lists, Markdown links)
- Link directly to release notes and other documentation pages where relevant.
- When sharing docs references in reporting, make sure to link to the HTML pages.
- Report on both the methodology, and the outcome.
- Use artifacts in addition to messages if supported.

### Commit and pull request strategy

If the current task mode is to work directly on the project code, commit regularly on a new branch unless otherwise noted by project instructions.

Commit for:

- Version upgrades of dependencies
- Fixes in the code
- Fixes / additions in test suites
- Documentation updates

Push if allowed from current permissions or after user confirmation, when:

- We want to see results from Continuous Integration tools.
- We want human review.
- We think the work is done.

### Quality Assurance

Options to check that the upgrade works correctly, to use as needed through upgrade steps:

- Stylelint linting passes
- Stylesheets auto-formatting passes
- Other project-specific QA checks

Look for any deprecation warnings coming from Stylelint in particular.

### Definition of done

- Dependency files updated and consistent (`package.json` and lockfile)
- Test suite / QA tools / CI all passing
- No new deprecation warnings introduced (or explicitly documented)
- Any relevant project doc is updated
- Upgrade report created

## Steps

### Confirm upgrade path

- [ ] Confirm all input sources from the upgrade methodology.
- [ ] Retrieve the current Node / Stylelint versions from context or user input
- [ ] Determine the target Stylelint version ("latest" or a specific version number)
- [ ] Fetch [Stylelint migration guides](https://github.com/stylelint/stylelint/tree/main/docs/migration-guide) and use the listing to confirm which releases are along the upgrade path, from current to target.
- [ ] Retrieve the current versions of any other "stylelint" package installed.
- [ ] Find the CHANGELOG documents for those Stylelint packages, to understand their compatibility with different Stylelint versions.
- [ ] Report the upgrade path to the user.

At this stage, if there are multiple Stylelint versions on the upgrade path, make sure that all subsequent work is done in sequence for every one of those versions. For example, upgrading from Stylelint v14 to v16 should involve running through all the steps in this file with v15 as the target; then asking the user to confirm the successful v15 upgrade; then restarting this all from v15 to v16.

### Baseline setup and QA

- [ ] Check for project-specific information about quality assurance tools and methodologies, dependencies management, and upgrades considerations.
- [ ] Create a branch for the upgrade (check any conventions for branch names, or `upgrade-stylelint-vX`)
- [ ] Run the project’s QA tools to capture a baseline. At least linting.

### Dependencies audit and upgrades

This may need to be done in a different order depending on whether dependency compatibility issues are reported when upgrading to the new Stylelint version.

- [ ] Use `npm info . devDependencies` to confirm the current versions of all of the project’s dependencies ahead of the upgrades.
- [ ] From the CHANGELOGs of Stylelint-related dependencies, check which versions of each package is compatible with our target Stylelint version, and any upgrade considerations we need to take into account.
- [ ] Use `npm install --save-dev stylelint@<version>` to install the target Stylelint version, including any other packages relevant to that project.
- [ ] Report the needed dependencies upgrades to the user
- [ ] Use the project’s QA tools / test suite as needed when doing the upgrades, to confirm the results.

Note any warnings or errors from npm or from the project’s QA tools. Those might indicate further actions needed for the upgrades to be successful. Those might require moving on to the subsequent steps to resolve.

### Apply official upgrade guidance

- [ ] Fetch the Stylelint CHANGELOG and migration guide from the next version on the upgrade path, from the official docs.
- [ ] Review the required actions and think about which ones are likely to affect this project.
- [ ] Keep the project’s Node version as-is if it’s already higher than the Stylelint support.
- [ ] Review the project’s implementation of Stylelint APIs and CLI usage, to identify possible code or docs that needs changes.
- [ ] Report those findings. Consider providing a "Status" for every entry in the migration guide, even if just to report the current project is "Not affected"

### Stylesheets and rules updates

This is crucial for the success of the upgrade. The upgrade of Stylelint or of related packages may include changes to linting rules, which might surface new issues with the project.

- [ ] Run the linting to confirm which styles might now have issues surfaced.
- [ ] Run Stylelint with `--fix lax` to attempt automated fixes if any are available.
- [ ] For remaining errors, if it seems safe to do so, attempt a manual fix based on the intent of the code and any messaging from Stylelint.
- [ ] Report any changes that seem like they might not be guaranteed to be safe to implement, for extended review.
- [ ] If some errors are too widespread or too dangerous to address, consider disabling the relevant rules via stylelint-disable code comments, or directly in the configuration file.

### Update documentation

- [ ] Review whether there is any project documentation to update, based on the changes needed for the upgrade. Make necessary changes if so.

### Produce the upgrade report

- [ ] Check specific instructions from the user / coding harness on how to report information.
- [ ] Report on any assumptions taken while interpreting the methodology for upgrades.
- [ ] Add the reporting for every step in the upgrade process.
- [ ] Report on any opt-in changes from the Stylelint release notes that haven’t been applied.
- [ ] If it seems helpful, produce a manual test plan for the user.
- [ ] If it seems helpful, produce a recap of relevant changes that can be shared with users of this project.
