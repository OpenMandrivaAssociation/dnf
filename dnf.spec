#define snapshot 20220923
%define major 2
%define climajor 3
%define oldlibname %mklibname dnf5_ 1
%define oldclilibname %mklibname dnf5-cli 1
%define libname %mklibname dnf5
%define clilibname %mklibname dnf5-cli
%define devname %mklibname -d dnf5

# (bero) dnf5 is now ready to replace dnf
%bcond_without dnf5_default
%bcond_without ruby

Summary: Command-line package manager
Name: dnf
Version: 5.4.8.0
Release: %{?snapshot:0.%{snapshot}.}1
URL: https://github.com/rpm-software-management/dnf5
License: GPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.0-or-later
Group: System/Configuration/Packaging
%if 0%{?snapshot:1}
Source0: https://github.com/rpm-software-management/dnf5/archive/refs/heads/main.tar.gz#/%{name}-%{snapshot}.tar.gz
%else
Source0: https://github.com/rpm-software-management/dnf5/archive/refs/tags/%{version}.tar.gz
%endif

BuildRequires: cmake >= 3.24
BuildRequires: ninja
BuildRequires: gettext
BuildRequires: cmake(toml11) >= 4.3.0
BuildRequires: pkgconfig(appstream) >= 0.16
BuildRequires: pkgconfig(fmt)
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(modulemd-2.0) >= 2.5.0
BuildRequires: pkgconfig(libsolv) >= 0.7.36
BuildRequires: pkgconfig(libsolvext) >= 0.7.36
BuildRequires: pkgconfig(rpm) >= 4.19.0
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(zck)
BuildRequires: pkgconfig(glib-2.0) >= 2.46.0
BuildRequires: pkgconfig(gpgme)
BuildRequires: pkgconfig(librepo) >= 1.22.0
BuildRequires: pkgconfig(sqlite3) >= 3.35.0
BuildRequires: pkgconfig(smartcols)
BuildRequires: pkgconfig(sdbus-c++) >= 0.9.0
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(libcurl) >= 7.62.0
BuildRequires: pkgconfig(ldap)
BuildRequires: pkgconfig(libacl)
BuildRequires: pkgconfig(libpkgmanifest) >= 0.5.10
BuildRequires: bash-completion-devel
BuildRequires: createrepo_c
# /usr/bin/clang-scan-deps
BuildRequires: clang-tools
# Language bindings & test tooling
%if !%{cross_compiling}
BuildRequires: perl-devel
BuildRequires: perl(FindBin)
BuildRequires: perl(Test::Exception)
BuildRequires: perl(Test::More)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)
BuildRequires: pkgconfig(cppunit)
%endif
BuildRequires: pkgconfig(python3)
%if %{with ruby}
BuildRequires: ruby-devel
%endif
BuildRequires: swig >= 4.3
# For building man pages
BuildRequires: python%{pyver}dist(sphinx) >= 4.1.2
BuildRequires: python%{pyver}dist(breathe)
%if %{without dnf5_default}
Requires: dnf-data
%endif
Recommends: bash-completion
Recommends: %{name}-plugin-manifest = %{EVRD}
Requires: %{libname} = %{EVRD}
Requires: %{clilibname} = %{EVRD}
%rename microdnf

%if %{with dnf5_default}
Provides: yum = %{EVRD}
Obsoletes: yum < 5
%rename dnf5
%endif

Provides: dnf5-command(install) = %{EVRD}
Provides: dnf5-command(upgrade) = %{EVRD}
Provides: dnf5-command(remove) = %{EVRD}
Provides: dnf5-command(distro-sync) = %{EVRD}
Provides: dnf5-command(downgrade) = %{EVRD}
Provides: dnf5-command(reinstall) = %{EVRD}
Provides: dnf5-command(swap) = %{EVRD}
Provides: dnf5-command(mark) = %{EVRD}
Provides: dnf5-command(autoremove) = %{EVRD}
Provides: dnf5-command(check-upgrade) = %{EVRD}
Provides: dnf5-command(leaves) = %{EVRD}
Provides: dnf5-command(repoquery) = %{EVRD}
Provides: dnf5-command(search) = %{EVRD}
Provides: dnf5-command(status) = %{EVRD}
Provides: dnf5-command(list) = %{EVRD}
Provides: dnf5-command(info) = %{EVRD}
Provides: dnf5-command(group) = %{EVRD}
Provides: dnf5-command(environment) = %{EVRD}
Provides: dnf5-command(module) = %{EVRD}
Provides: dnf5-command(history) = %{EVRD}
Provides: dnf5-command(repo) = %{EVRD}
Provides: dnf5-command(advisory) = %{EVRD}
Provides: dnf5-command(clean) = %{EVRD}
Provides: dnf5-command(download) = %{EVRD}
Provides: dnf5-command(makecache) = %{EVRD}
Provides: dnf5-command(builddep) = %{EVRD}
Provides: dnf5-command(changelog) = %{EVRD}
Provides: dnf5-command(copr) = %{EVRD}
Provides: dnf5-command(config-manager) = %{EVRD}
Provides: dnf5-command(debuginfo-install) = %{EVRD}
Provides: dnf5-command(deptree) = %{EVRD}
Provides: dnf5-command(do) = %{EVRD}
Provides: dnf5-command(needs-restarting) = %{EVRD}
Provides: dnf5-command(offline) = %{EVRD}
Provides: dnf5-command(repoclosure) = %{EVRD}
Provides: dnf5-command(repomanage) = %{EVRD}
Provides: dnf5-command(replay) = %{EVRD}
Provides: dnf5-command(reposync) = %{EVRD}
Provides: dnf5-command(check) = %{EVRD}
Provides: dnf5-command(provides) = %{EVRD}
Provides: dnf5-command(system-upgrade) = %{EVRD}
Provides: dnf5-command(versionlock) = %{EVRD}
# Aliases
Provides: dnf5-command(rm) = %{EVRD}
Provides: dnf5-command(erase) = %{EVRD}
Provides: dnf5-command(dsync) = %{EVRD}

%patchlist
dnf5-znver1.patch
dnf5-distro-release.patch
# Bring back dnf 4.x's --ref shortcut (meaning --refresh)
dnf5-ref.patch
# and "dnf erase" (used to mean "dnf rm")
dnf5-erase.patch
dnf5-workaround-rpmtsRun-exit-code.patch
# Upstream post-5.4.8.0 fixes (CVE-2026-123177, RPM log propagation, RPM header hygiene)
dnf5-5.4.8.0-CVE-2026-123177-1.patch
dnf5-5.4.8.0-CVE-2026-123177-2.patch
dnf5-5.4.8.0-propagate-rpm-logs.patch
dnf5-5.4.8.0-rpmcrypto-header.patch
dnf5-5.4.8.0-lock-system-repo-mkdir.patch

%description
DNF5 is a command-line package manager that automates the process of installing,
upgrading, configuring, and removing computer programs in a consistent manner.
It supports RPM packages, modulemd modules, and comps groups & environments

%package plugin-automatic
Summary: DNF5 plugin for automatic updates
Group: System
Requires: %{name} = %{EVRD}
Conflicts: %{name} < 5.4.8.0
Provides: dnf5-command(automatic) = %{EVRD}
%rename dnf5-plugin-automatic

%description plugin-automatic
Alternative CLI to dnf upgrade with specific facilities to make it suitable
to be executed automatically and regularly from systemd timers, cron jobs
and similar.

%package plugin-manifest
Summary: DNF5 plugin for working with RPM package manifest files
Group: System
Requires: %{name} = %{EVRD}
Requires: %{mklibname pkgmanifest} >= 0.5.10
Conflicts: %{name} < 5.4.8.0
Provides: dnf5-command(manifest) = %{EVRD}
%rename dnf5-plugin-manifest

%description plugin-manifest
DNF5 plugin for working with RPM package manifest files.

%package plugin-appstream
Summary: DNF5 plugin for handling AppStream metadata
Group: System
Requires: %{name} = %{EVRD}
Provides: dnf5-command(appstream) = %{EVRD}
%rename dnf5-plugin-appstream

%description plugin-appstream
DNF5 plugin for installing and removing AppStream metadata alongside
repository operations.

%package plugin-expired-pgp-keys
Summary: DNF5 plugin for detecting expired PGP keys
Group: System
Requires: %{name} = %{EVRD}
Provides: dnf5-command(expired-pgp-keys) = %{EVRD}
%rename dnf5-plugin-expired-pgp-keys

%description plugin-expired-pgp-keys
DNF5 plugin for checking for expired OpenPGP keys in the RPM database and
offering to remove them.

%package plugin-local
Summary: DNF5 plugin for creating a local DNF repository from downloaded packages
Group: System
Requires: %{name} = %{EVRD}
Requires: createrepo_c

%description plugin-local
DNF5 plugin that copies downloaded packages into a local directory and
regenerates repository metadata for offline or shared reuse.

%package plugin-python
Summary: DNF5 plugin for supporting plugins written in Python
Group: System
Requires: %{name} = %{EVRD}
Requires: python-%{name} = %{EVRD}

%description plugin-python
Libdnf5 plugin loader that allows extending DNF5 and libdnf5 with plugins
written in Python.

%package plugin-systemd-inhibit
Summary: Libdnf5 plugin that prevents system shutdown during a package transaction
Group: System
Requires: %{libname} = %{EVRD}
Provides: libdnf5-plugin-systemd-inhibit = %{EVRD}

%description plugin-systemd-inhibit
Libdnf5 plugin that acquires a systemd inhibitor lock during a package
transaction to prevent system shutdown or reboot while packages are being
installed, removed, or updated.

%package -n %{libname}
Summary: Package management library
Group: System/Libraries
%if %{with dnf5_default}
Conflicts: dnf-data < 4.16.0
%endif
Requires: %{_sysconfdir}/dnf/dnf.conf
Requires: %{mklibname repo} >= 1.22.0
Recommends: %{name}-plugin-systemd-inhibit = %{EVRD}
%rename %{_lib}dnf1
%rename %{oldlibname}

%description -n %{libname}
Package management library.

%package -n %{clilibname}
Summary: Library for working with a terminal in a command-line package manager
Group: System/Libraries
%rename %{_lib}dnf-cli
%rename %{_lib}dnf-cli1
%rename %{oldclilibname}

%description -n %{clilibname}
Library for working with a terminal in a command-line package manager.

%package -n dnf5daemon-client
Summary: Command-line interface for dnf5daemon-server
Requires: dnf5daemon-server
Conflicts: dnf5 < 5.0.0

%description -n dnf5daemon-client
Command-line interface for dnf5daemon-server.

%package -n dnf5daemon-server
Summary: Package management service with a DBus interface
Requires: %{libname} >= %{EVRD}
Requires: %{clilibname} >= %{EVRD}
Conflicts: dnf5 < 5.0.0
Requires: dbus
Requires: polkit
%if %{without dnf5_default}
Requires: dnf-data
%endif

%description -n dnf5daemon-server
Package management service with a DBus interface.

%package -n %{devname}
Summary: Development files for the DNF package management library
Group: Development/C++ and C
Requires: %{libname} = %{EVRD}
Requires: %{clilibname} = %{EVRD}

%description -n %{devname}
Development files for the DNF package management library.

%package -n python-%{name}
Summary: Python language bindings to the DNF package manager
Group: Development/Python
%rename python-dnf5

%description -n python-%{name}
Python language bindings to the DNF package manager.

%if !%{cross_compiling}
%package -n perl-%{name}
Summary: Perl language bindings to the DNF package manager
Group: Development/Perl
%rename perl-dnf5

%description -n perl-%{name}
Perl language bindings to the DNF package manager.
%endif

%package -n ruby-%{name}
Summary: Ruby language bindings to the DNF package manager
Group: Development/Ruby
%rename ruby-dnf5

%description -n ruby-%{name}
Ruby language bindings to the DNF package manager.

%prep
%autosetup -p1 -n %{?snapshot:dnf-main}%{!?snapshot:%{name}5-%{version}}
%if %{cross_compiling}
TOP="$(pwd)"
# FIXME this should be fixed properly, but for now, this
# is the fastest way to limit the damage of an added
# -I/usr/include
find . -name CMakeLists.txt |xargs \
	sed -i -e 's/include_directories(\${LIBXML2/#&/g' -e 's/include_directories(\${GLIB/#&/g' -e 's/include_directories(\${JSONC/#&/g' -e 's/include_directories(\${REPO/#&/g' -e 's/include_directories(\${APPSTREAM/#&/g'
%global optflags %{optflags} -I%{_prefix}/%{_target_platform}/include/glib-2.0 -I%{_prefix}/%{_target_platform}/include/gio-unix-2.0 -I%{_prefix}/%{_target_platform}/%{_lib}/glib-2.0/include -I%{_prefix}/%{_target_platform}/include/libxml2 -I%{_prefix}/%{_target_platform}/include/json-c -I%{_prefix}/%{_target_platform}/include/appstream -Wno-error=vla-cxx-extension
# Since we point at HOST python when crosscompiling, we don't need
# an emulator to run $PYTHON in. But the python cmake modules barf
# if CMAKE_CROSSCOMPILING_EMULATOR isn't set, so let's point it at
# a script that does nothing.
cat >fakeemu <<'EOF'
#!/bin/bash
APP="$1"
shift
exec "$APP" "$@"
EOF
chmod +x fakeemu
%endif

%cmake \
	--compile-no-warning-as-error \
	-G Ninja \
	-DWITH_PLUGIN_RHSM_CONTAINER=OFF \
	-DWITH_HTML:BOOL=OFF \
	-DWITH_MAN:BOOL=ON \
	-DSYSTEMD_DIR=%{_unitdir} \
	-DTMPFILES_DIR=%{_tmpfilesdir} \
	-DPERL_INSTALLDIRS=vendor \
%if %{with ruby}
	-DRuby_VENDORARCH_DIR=$(ruby -e 'print $:[3]') \
	-DRuby_VENDORLIBDIR=$(ruby -e 'print $:[5]') \
%else
	-DWITH_RUBY:BOOL=OFF \
%endif
	-DPython3_EXECUTABLE=%{_bindir}/python \
%if %{cross_compiling}
	-DWITH_PERL5:BOOL=OFF \
	-DCMAKE_CROSSCOMPILING_EMULATOR="${TOP}/fakeemu" \
	-DPERL_EXECUTABLE=%{_prefix}/%{_target_platform}/usr/bin/perl \
	-DPERL_INCLUDE_PATH=%{_prefix}/%{_target_platform}/%{_lib}/perl5/CORE \
	-DPERL_LIBRARY=%{_prefix}/%{_target_platform}/%{_lib}/libperl.so \
	-DGETTEXT_MSGMERGE_EXECUTABLE=%{_bindir}/msgmerge \
	-DGETTEXT_MSGFMT_EXECUTABLE=%{_bindir}/msgfmt \
	-DWITH_TESTS:BOOL=OFF \
%else
	-DPERL_EXECUTABLE=%{_bindir}/perl \
%endif
	-DPKG_CONFIG_EXECUTABLE=%{_bindir}/pkg-config

%build
%ninja_build -C build
%ninja_build -C build doc-man

%install
%ninja_install -C build

# We don't need the README -- we know it's a plugin drop dir
rm %{buildroot}%{python_sitelib}/libdnf_plugins/README

%if %{with dnf5_default}
ln -sr %{buildroot}%{_bindir}/dnf5 %{buildroot}%{_bindir}/dnf
ln -sr %{buildroot}%{_bindir}/dnf5 %{buildroot}%{_bindir}/yum
ln -s dnf5 %{buildroot}%{_datadir}/bash-completion/completions/dnf
for file in %{buildroot}%{_mandir}/man[578]/dnf5[-.]*; do
	dir="$(dirname "$file")"
	filename="$(basename "$file")"
	ln -sr "$file" "$dir/${filename/dnf5/dnf}"
done
ln -sr %{buildroot}%{_mandir}/man8/dnf5.8 %{buildroot}%{_mandir}/man8/yum.8
%endif

ln -sr %{buildroot}%{_bindir}/dnf5 %{buildroot}%{_bindir}/microdnf
ln -sr %{buildroot}%{_mandir}/man8/dnf5.8 %{buildroot}%{_mandir}/man8/microdnf.8

# Enable offline transaction service in system-update.target
mkdir -p %{buildroot}%{_unitdir}/system-update.target.wants
ln -sr %{buildroot}%{_unitdir}/dnf5-offline-transaction.service %{buildroot}%{_unitdir}/system-update.target.wants/dnf5-offline-transaction.service

# Own dirs and files that dnf5 creates on runtime
mkdir -p %{buildroot}%{_prefix}/lib/sysimage/libdnf5
for file in \
	environments.toml groups.toml modules.toml nevras.toml packages.toml system.toml \
	transaction_history.sqlite transaction_history.sqlite-shm transaction_history.sqlite-wal
do
	touch %{buildroot}%{_prefix}/lib/sysimage/libdnf5/$file
done
mkdir -p %{buildroot}%{_prefix}/lib/sysimage/libdnf5/comps_groups
mkdir -p %{buildroot}%{_prefix}/lib/sysimage/libdnf5/offline
touch %{buildroot}%{_sysconfdir}/dnf/versionlock.toml
mkdir -p %{buildroot}%{_localstatedir}/lib/dnf
touch %{buildroot}%{_localstatedir}/lib/dnf/system-repo.lock

# We get this from distro-release -- to make sure $releasever is set
# correctly and to share the file between dnf4 and dnf5
rm %{buildroot}%{_sysconfdir}/dnf/dnf.conf

%find_lang dnf5
%find_lang dnf5-plugin-automatic
%find_lang dnf5-plugin-builddep
%find_lang dnf5-plugin-changelog
%find_lang dnf5-plugin-config-manager
%find_lang dnf5-plugin-copr
%find_lang dnf5-plugin-deptree
%find_lang dnf5-plugin-needs-restarting
%find_lang dnf5-plugin-repoclosure
%find_lang dnf5-plugin-reposync
%find_lang dnf5daemon-client
%find_lang dnf5daemon-server
%find_lang libdnf5
%find_lang libdnf5-cli
%find_lang libdnf5-plugin-actions
%find_lang libdnf5-plugin-expired-pgp-keys

%post
%systemd_post dnf5-makecache.timer

%preun
%systemd_preun dnf5-makecache.timer

%postun
%systemd_postun_with_restart dnf5-makecache.timer

%post -n dnf5daemon-server
%systemd_post dnf5daemon-server.service

%preun -n dnf5daemon-server
%systemd_preun dnf5daemon-server.service

%postun -n dnf5daemon-server
%systemd_postun_with_restart dnf5daemon-server.service

%if !%{cross_compiling}
%check
LD_LIBRARY_PATH="%{buildroot}%{_libdir}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ctest --test-dir build --output-on-failure -R '^(test_libdnf|test_libdnf_cli_|test_automatic|test_copr|test_needs_restarting)'
%endif

%files -f dnf5.lang -f dnf5-plugin-builddep.lang -f dnf5-plugin-changelog.lang -f dnf5-plugin-config-manager.lang -f dnf5-plugin-copr.lang -f dnf5-plugin-deptree.lang -f dnf5-plugin-needs-restarting.lang -f dnf5-plugin-repoclosure.lang -f libdnf5-plugin-actions.lang -f dnf5-plugin-reposync.lang
%dir %{_sysconfdir}/dnf
%dir %{_sysconfdir}/dnf/dnf5-aliases.d
%doc %{_sysconfdir}/dnf/dnf5-aliases.d/README
%dir %{_sysconfdir}/dnf/dnf5-plugins
%dir %{_datadir}/dnf5
%dir %{_datadir}/dnf5/aliases.d
%dir %{_datadir}/dnf5/dnf5-plugins
%{_datadir}/dnf5/aliases.d/compatibility-plugins.conf
%{_datadir}/dnf5/aliases.d/compatibility-reposync.conf
%{_datadir}/dnf5/aliases.d/compatibility.conf
%{_bindir}/dnf5
%{_bindir}/microdnf
%if %{with dnf5_default}
%{_bindir}/dnf
%{_bindir}/yum
%{_datadir}/bash-completion/completions/dnf
%doc %{_mandir}/man8/dnf.8*
%doc %{_mandir}/man8/yum.8*
%endif
%doc %{_mandir}/man8/microdnf.8*
%{_datadir}/bash-completion/completions/dnf5
%{_datadir}/zsh/site-functions/_dnf5
%dir %{_libdir}/dnf5
%dir %{_libdir}/dnf5/plugins
%doc %{_libdir}/dnf5/plugins/README
%{_libdir}/dnf5/plugins/builddep_cmd_plugin.so
%{_libdir}/dnf5/plugins/changelog_cmd_plugin.so
%{_libdir}/dnf5/plugins/config-manager_cmd_plugin.so
%{_libdir}/dnf5/plugins/copr_cmd_plugin.so
%{_libdir}/dnf5/plugins/deptree_cmd_plugin.so
%{_libdir}/dnf5/plugins/needs_restarting_cmd_plugin.so
%{_libdir}/dnf5/plugins/repoclosure_cmd_plugin.so
%{_libdir}/dnf5/plugins/repomanage_cmd_plugin.so
%{_libdir}/dnf5/plugins/reposync_cmd_plugin.so
%{_libdir}/libdnf5/plugins/actions.so
%config(noreplace) %{_sysconfdir}/dnf/libdnf5-plugins/actions.conf
%dir %{_sysconfdir}/dnf/libdnf5-plugins/actions.d
%{_unitdir}/dnf5-makecache.service
%{_unitdir}/dnf5-makecache.timer
%{_unitdir}/dnf5-offline-transaction.service
%{_unitdir}/dnf5-offline-transaction-cleanup.service
%{_unitdir}/system-update.target.wants/dnf5-offline-transaction.service
%doc %{_mandir}/man5/dnf*.conf.5*
%doc %{_mandir}/man5/dnf*.conf-todo.5*
%doc %{_mandir}/man5/dnf*.conf-deprecated.5*
%doc %{_mandir}/man5/dnf*.conf-vendorpolicy.5*
%doc %{_mandir}/man5/dnf*.conf-vendorpolicy-v1_0.5*
%doc %{_mandir}/man5/dnf*.conf-vendorpolicy-v1_1.5*
%doc %{_mandir}/man8/libdnf5-actions.8*
%doc %{_mandir}/man7/dnf*.7*
%doc %{_mandir}/man8/dnf5.8*
%doc %{_mandir}/man8/dnf5-advisory.8*
%doc %{_mandir}/man8/dnf5-autoremove.8*
%doc %{_mandir}/man8/dnf5-builddep.8*
%doc %{_mandir}/man8/dnf5-changelog.8*
%doc %{_mandir}/man8/dnf5-check.8*
%doc %{_mandir}/man8/dnf5-check-upgrade.8*
%doc %{_mandir}/man8/dnf5-clean.8*
%doc %{_mandir}/man8/dnf5-config-manager.8*
%doc %{_mandir}/man8/dnf5-copr.8*
%doc %{_mandir}/man8/dnf5-debuginfo-install.8*
%doc %{_mandir}/man8/dnf5-deptree.8*
%doc %{_mandir}/man8/dnf5-distro-sync.8*
%doc %{_mandir}/man8/dnf5-do.8*
%doc %{_mandir}/man8/dnf5-downgrade.8*
%doc %{_mandir}/man8/dnf5-download.8*
%doc %{_mandir}/man8/dnf5-environment.8*
%doc %{_mandir}/man8/dnf5-group.8*
%doc %{_mandir}/man8/dnf5-history.8*
%doc %{_mandir}/man8/dnf5-info.8*
%doc %{_mandir}/man8/dnf5-install.8*
%doc %{_mandir}/man8/dnf5-leaves.8*
%doc %{_mandir}/man8/dnf5-list.8*
%doc %{_mandir}/man8/dnf5-makecache.8*
%doc %{_mandir}/man8/dnf5-mark.8*
%doc %{_mandir}/man8/dnf5-module.8*
%doc %{_mandir}/man8/dnf5-needs-restarting.8*
%doc %{_mandir}/man8/dnf5-offline.8*
%doc %{_mandir}/man8/dnf5-provides.8*
%doc %{_mandir}/man8/dnf5-reinstall.8*
%doc %{_mandir}/man8/dnf5-remove.8*
%doc %{_mandir}/man8/dnf5-replay.8*
%doc %{_mandir}/man8/dnf5-repo.8*
%doc %{_mandir}/man8/dnf5-repoclosure.8*
%doc %{_mandir}/man8/dnf5-repomanage.8*
%doc %{_mandir}/man8/dnf5-repoquery.8*
%doc %{_mandir}/man8/dnf5-reposync.8*
%doc %{_mandir}/man8/dnf5-search.8*
%doc %{_mandir}/man8/dnf5-status.8*
%doc %{_mandir}/man8/dnf5-swap.8*
%doc %{_mandir}/man8/dnf5-system-upgrade.8*
%doc %{_mandir}/man8/dnf5-upgrade.8*
%doc %{_mandir}/man8/dnf5-versionlock.8*
%if %{with dnf5_default}
%doc %{_mandir}/man8/dnf-advisory.8*
%doc %{_mandir}/man8/dnf-autoremove.8*
%doc %{_mandir}/man8/dnf-builddep.8*
%doc %{_mandir}/man8/dnf-changelog.8*
%doc %{_mandir}/man8/dnf-check.8*
%doc %{_mandir}/man8/dnf-check-upgrade.8*
%doc %{_mandir}/man8/dnf-clean.8*
%doc %{_mandir}/man8/dnf-config-manager.8*
%doc %{_mandir}/man8/dnf-copr.8*
%doc %{_mandir}/man8/dnf-debuginfo-install.8*
%doc %{_mandir}/man8/dnf-deptree.8*
%doc %{_mandir}/man8/dnf-distro-sync.8*
%doc %{_mandir}/man8/dnf-do.8*
%doc %{_mandir}/man8/dnf-downgrade.8*
%doc %{_mandir}/man8/dnf-download.8*
%doc %{_mandir}/man8/dnf-environment.8*
%doc %{_mandir}/man8/dnf-group.8*
%doc %{_mandir}/man8/dnf-history.8*
%doc %{_mandir}/man8/dnf-info.8*
%doc %{_mandir}/man8/dnf-install.8*
%doc %{_mandir}/man8/dnf-leaves.8*
%doc %{_mandir}/man8/dnf-list.8*
%doc %{_mandir}/man8/dnf-makecache.8*
%doc %{_mandir}/man8/dnf-mark.8*
%doc %{_mandir}/man8/dnf-module.8*
%doc %{_mandir}/man8/dnf-needs-restarting.8*
%doc %{_mandir}/man8/dnf-offline.8*
%doc %{_mandir}/man8/dnf-provides.8*
%doc %{_mandir}/man8/dnf-reinstall.8*
%doc %{_mandir}/man8/dnf-remove.8*
%doc %{_mandir}/man8/dnf-replay.8*
%doc %{_mandir}/man8/dnf-repo.8*
%doc %{_mandir}/man8/dnf-repoclosure.8*
%doc %{_mandir}/man8/dnf-repomanage.8*
%doc %{_mandir}/man8/dnf-repoquery.8*
%doc %{_mandir}/man8/dnf-reposync.8*
%doc %{_mandir}/man8/dnf-search.8*
%doc %{_mandir}/man8/dnf-status.8*
%doc %{_mandir}/man8/dnf-swap.8*
%doc %{_mandir}/man8/dnf-system-upgrade.8*
%doc %{_mandir}/man8/dnf-upgrade.8*
%doc %{_mandir}/man8/dnf-versionlock.8*
%endif

%files plugin-automatic -f dnf5-plugin-automatic.lang
%{_bindir}/dnf-automatic
%{_libdir}/dnf5/plugins/automatic_cmd_plugin.so
%{_unitdir}/dnf-automatic.service
%{_unitdir}/dnf-automatic.timer
%{_unitdir}/dnf5-automatic.service
%{_unitdir}/dnf5-automatic.timer
%{_datadir}/dnf5/dnf5-plugins/automatic.conf
%{_datadir}/dbus-1/system.d/org.rpm.dnf.v0.Automatic.conf
%doc %{_mandir}/man8/dnf5-automatic.8*
%if %{with dnf5_default}
%doc %{_mandir}/man8/dnf-automatic.8*
%endif

%files plugin-manifest
%{_libdir}/dnf5/plugins/manifest_cmd_plugin.so
%doc %{_mandir}/man8/dnf5-manifest.8*
%if %{with dnf5_default}
%doc %{_mandir}/man8/dnf-manifest.8*
%endif

%files plugin-appstream
%config(noreplace) %{_sysconfdir}/dnf/libdnf5-plugins/appstream.conf
%{_libdir}/libdnf5/plugins/appstream.so

%files plugin-expired-pgp-keys -f libdnf5-plugin-expired-pgp-keys.lang
%config(noreplace) %{_sysconfdir}/dnf/libdnf5-plugins/expired-pgp-keys.conf
%{_libdir}/libdnf5/plugins/expired-pgp-keys.so
%doc %{_mandir}/man8/libdnf5-expired-pgp-keys.8*

%files plugin-local
%config(noreplace) %{_sysconfdir}/dnf/libdnf5-plugins/local.conf
%{_libdir}/libdnf5/plugins/local.so
%doc %{_mandir}/man8/libdnf5-local.8*

%files plugin-python
%config(noreplace) %{_sysconfdir}/dnf/libdnf5-plugins/python_plugins_loader.conf
%dir %{_sysconfdir}/dnf/libdnf5-plugins/python_plugins_loader.d
%{_libdir}/libdnf5/plugins/python_plugins_loader.*
%dir %{python_sitelib}/libdnf_plugins/

%files plugin-systemd-inhibit
%config(noreplace) %{_sysconfdir}/dnf/libdnf5-plugins/00-systemd-inhibit.conf
%{_libdir}/libdnf5/plugins/systemd-inhibit.so

%files -n %{libname} -f libdnf5.lang
%if %{with dnf5_default}
%dir %{_sysconfdir}/dnf/vars
%dir %{_sysconfdir}/dnf/protected.d
%dir %{_sysconfdir}/dnf/usr-drift-protected-paths.d
%endif
%ghost %attr(0644, root, root) %{_sysconfdir}/dnf/versionlock.toml
%dir %{_datadir}/dnf5/libdnf.conf.d
%dir %{_sysconfdir}/dnf/libdnf5.conf.d
%dir %{_datadir}/dnf5/repos.override.d
%dir %{_sysconfdir}/dnf/repos.override.d
%dir %{_datadir}/dnf5/repos.d
%dir %{_datadir}/dnf5/vars.d
%dir %{_datadir}/dnf5/vendors.d
%dir %{_datadir}/dnf5/libdnf.plugins.conf.d
%dir %{_sysconfdir}/dnf/vendors.d
%dir %{_sysconfdir}/dnf/suggest-reboot.d
%dir %{_datadir}/dnf5/suggest-reboot.d
%dir %{_sysconfdir}/dnf/libdnf5-plugins
%dir %{_libdir}/libdnf5
%dir %{_libdir}/libdnf5/plugins
%{_libdir}/libdnf5.so.%{major}*
%{_tmpfilesdir}/libdnf5.conf
%attr(0755, root, root) %dir %{_localstatedir}/lib/dnf
%ghost %verify(not md5 size mtime) %attr(0644, root, root) %{_localstatedir}/lib/dnf/system-repo.lock
%dir %{_prefix}/lib/sysimage/libdnf5
%attr(0755, root, root) %ghost %dir %{_prefix}/lib/sysimage/libdnf5/comps_groups
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/environments.toml
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/groups.toml
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/modules.toml
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/nevras.toml
%attr(0755, root, root) %ghost %dir %{_prefix}/lib/sysimage/libdnf5/offline
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/packages.toml
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/system.toml
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/transaction_history.sqlite
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/transaction_history.sqlite-shm
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/transaction_history.sqlite-wal

%files -n %{clilibname} -f libdnf5-cli.lang
%{_libdir}/libdnf5-cli.so.%{climajor}*

%files -n dnf5daemon-client -f dnf5daemon-client.lang
%{_bindir}/dnf5daemon-client
%doc %{_mandir}/man8/dnf5daemon-client.8*

%files -n dnf5daemon-server -f dnf5daemon-server.lang
%{_bindir}/dnf5daemon-server
%{_unitdir}/dnf5daemon-server.service
%{_datadir}/dbus-1/system.d/org.rpm.dnf.v0.conf
%{_datadir}/dbus-1/system-services/org.rpm.dnf.v0.service
%{_datadir}/dbus-1/interfaces/org.rpm.dnf.v0.*.xml
%{_datadir}/polkit-1/actions/org.rpm.dnf.v0.policy
%{_datadir}/polkit-1/rules.d/org.rpm.dnf.v0.rules
%config(noreplace) %{_sysconfdir}/dnf/dnf5daemon-server.conf
%doc %{_mandir}/man8/dnf5daemon-server.8*
%doc %{_mandir}/man8/dnf5daemon-dbus-api.8*

%files -n %{devname}
%{_includedir}/libdnf5-cli
%{_includedir}/libdnf5
%dir %{_includedir}/dnf5
%{_includedir}/dnf5/*.h
%{_includedir}/dnf5/*.hpp
%{_libdir}/libdnf5-cli.so
%{_libdir}/libdnf5.so
%{_libdir}/pkgconfig/libdnf5.pc
%{_libdir}/pkgconfig/libdnf5-cli.pc

%files -n python-%{name}
%{python_sitearch}/libdnf5
%{python_sitearch}/libdnf5-*.dist-info
%{python_sitearch}/libdnf5_cli
%{python_sitearch}/libdnf5_cli-*.dist-info

%if !%{cross_compiling}
%files -n perl-%{name}
%{_libdir}/perl5/vendor_perl/auto/libdnf5
%{_libdir}/perl5/vendor_perl/auto/libdnf5_cli
%{_libdir}/perl5/vendor_perl/libdnf5
%{_libdir}/perl5/vendor_perl/libdnf5_cli
%endif

%if %{with ruby}
%files -n ruby-%{name}
%{_libdir}/ruby/vendor_ruby/*/*
%endif
