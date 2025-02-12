#define snapshot 20220923
%define major 2
%define oldlibname %mklibname dnf5_ 1
%define oldclilibname %mklibname dnf5-cli 1
%define libname %mklibname dnf5
%define clilibname %mklibname dnf5-cli
%define devname %mklibname -d dnf5
%global optflags %{optflags} -Wno-error=vla-cxx-extension

# (tpg) dnf5 is not yet ready to replace dnf
%bcond_with dnf5_default
%bcond_without ruby

Summary: Command-line package manager
Name: dnf5
Version: 5.2.10.0
Release: %{?snapshot:0.%{snapshot}.}2
URL: https://github.com/rpm-software-management/dnf5
License: GPL
Group: System/Configuration/Packaging
%if 0%{?snapshot:1}
Source0: https://github.com/rpm-software-management/dnf5/archive/refs/heads/main.tar.gz#/%{name}-%{snapshot}.tar.gz
%else
Source0: https://github.com/rpm-software-management/dnf5/archive/refs/tags/%{version}.tar.gz
%endif
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: gettext
BuildRequires: cmake(toml11)
BuildRequires: perl(Test::Exception)
BuildRequires: pkgconfig(appstream) >= 0.16
BuildRequires: pkgconfig(libcomps)
BuildRequires: pkgconfig(fmt)
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(modulemd-2.0)
BuildRequires: pkgconfig(libsolv) >= 0.7.25
BuildRequires: pkgconfig(libsolvext)
BuildRequires: pkgconfig(rpm)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(zck)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gpgme)
BuildRequires: pkgconfig(librepo)
BuildRequires: pkgconfig(sqlite3) >= 3.35.0
BuildRequires: pkgconfig(smartcols)
BuildRequires: pkgconfig(sdbus-c++)
BuildRequires: pkgconfig(cppunit)
BuildRequires: pkgconfig(libcurl)
BuildRequires: cmake(bash-completion)
BuildRequires: gettext
BuildRequires: createrepo_c
# For -lstdc++fs, but is that really needed?
BuildRequires: stdc++-static-devel
# /usr/bin/clang-scan-deps
BuildRequires: clang-tools
# Language bindings
BuildRequires: perl-devel
BuildRequires: pkgconfig(python3)
%if %{with ruby}
BuildRequires: ruby-devel
%endif
BuildRequires: swig
# For building man pages
BuildRequires: python-sphinx
BuildRequires: python3dist(breathe)
%if %{without dnf5_default}
Requires: dnf-data
%endif
Recommends: bash-completion
%rename microdnf

%if %{with dnf5_default}
Provides: dnf = %{EVRD}
Obsoletes: dnf < 5
Provides: yum = %{EVRD}
Obsoletes: yum < 5
%endif

Provides: dnf5-command(install)
Provides: dnf5-command(upgrade)
Provides: dnf5-command(remove)
Provides: dnf5-command(distro-sync)
Provides: dnf5-command(downgrade)
Provides: dnf5-command(reinstall)
Provides: dnf5-command(swap)
Provides: dnf5-command(mark)
Provides: dnf5-command(autoremove)
Provides: dnf5-command(check-upgrade)
Provides: dnf5-command(leaves)
Provides: dnf5-command(repoquery)
Provides: dnf5-command(search)
Provides: dnf5-command(list)
Provides: dnf5-command(info)
Provides: dnf5-command(group)
Provides: dnf5-command(environment)
Provides: dnf5-command(module)
Provides: dnf5-command(history)
Provides: dnf5-command(repo)
Provides: dnf5-command(advisory)
Provides: dnf5-command(clean)
Provides: dnf5-command(download)
Provides: dnf5-command(makecache)
Provides: dnf5-command(builddep)
Provides: dnf5-command(changelog)
Provides: dnf5-command(copr)
Provides: dnf5-command(config-manager)
Provides: dnf5-command(needs-restarting)
Provides: dnf5-command(repoclosure)
Provides: dnf5-command(check)
Provides: dnf5-command(provides)
# Aliases
Provides: dnf5-command(rm)
Provides: dnf5-command(erase)
Provides: dnf5-command(dsync)

%patchlist
dnf5-znver1.patch
dnf5-distro-release.patch
# Bring back dnf 4.x's --ref shortcut (meaning --refresh)
dnf5-ref.patch
dnf5-erase.patch
# sdbus-cpp 2.0 support from master branch
https://github.com/rpm-software-management/dnf5/commit/1e1a0627a5102f13f5e4515823ef2305bd4e9763.patch
https://github.com/rpm-software-management/dnf5/commit/cdf99383de790a1c7497f297094c156b9b862d86.patch
https://github.com/rpm-software-management/dnf5/commit/af00463e6449f796dad0e4a4da2cb86a6373eb72.patch
https://github.com/rpm-software-management/dnf5/commit/4714a43af45942a033caff85b8b1d5d9983c7035.patch
https://github.com/rpm-software-management/dnf5/commit/270094934dc6ecfce6136eb24c872757723c42ea.patch
https://github.com/rpm-software-management/dnf5/commit/fb9cea1132b03fc22439d0e3f0d38e5240697ea7.patch
https://github.com/rpm-software-management/dnf5/commit/c5df756b2e1a5c82801a24b9a296e5881ec80a70.patch
https://github.com/rpm-software-management/dnf5/commit/60e5a6bbf4172079fb72aadbc3021a3de3cf937e.patch
https://github.com/rpm-software-management/dnf5/commit/4eb8ef299690ab4795f73d06bdf5883dc0a34f02.patch
# Other relevant patches from master
https://github.com/rpm-software-management/dnf5/commit/ec6c1d829ab19cfb40b3b1c58d419c8fdef56b0c.patch
https://github.com/rpm-software-management/dnf5/commit/282d0c60ddcf39b813c2bc8de9482bfe69c84866.patch
https://github.com/rpm-software-management/dnf5/commit/76c2d994f507e2558ca26134b87042ac930793ce.patch

%description
DNF5 is a command-line package manager that automates the process of installing,
upgrading, configuring, and removing computer programs in a consistent manner.
It supports RPM packages, modulemd modules, and comps groups & environments

%package plugin-automatic
Summary: dnf5 plugin for automatic updates
Group: System
Requires: %{name} = %{EVRD}
Provides: dnf5-command(automatic)

%description plugin-automatic
Alternative CLI to dnf upgrade with specific facilities to make it suitable
to be executed automatically and regularly from systemd timers, cron jobs
and similar.

%package plugin-appstream
Summary: dnf5 plugin for handling appstream metadata
Group: System
Requires: %{name} = %{EVRD}
Provides: dnf5-command(appstream)

%description plugin-appstream
DNF plugin for handling appstream metadata

%package plugin-expired-pgp-keys
Summary: dnf5 plugin for detecting expired pgp keys
Group: System
Requires: %{name} = %{EVRD}
Provides: dnf5-command(expired-pgp-keys)

%description plugin-expired-pgp-keys
DNF plugin for detecting expired pgp keys

%package -n %{libname}
Summary: Package management library
Group: System/Libraries
%if %{with dnf5_default}
Conflicts: dnf-data < 4.16.0
%endif
Requires: %{_sysconfdir}/dnf/dnf.conf
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

%description -n python-%{name}
Python language bindings to the DNF package manager.

%package -n perl-%{name}
Summary: Perl language bindings to the DNF package manager
Group: Development/Perl

%description -n perl-%{name}
Perl language bindings to the DNF package manager.

%package -n ruby-%{name}
Summary: Ruby language bindings to the DNF package manager
Group: Development/Ruby

%description -n ruby-%{name}
Ruby language bindings to the DNF package manager.

%prep
%autosetup -p1 -n %{?snapshot:dnf-main}%{!?snapshot:%{name}-%{version}}
%if %{cross_compiling}
# FIXME this should be fixed properly, but for now, this
# is the fastest way to limit the damage of an added
# -I/usr/include
find . -name CMakeLists.txt |xargs \
	sed -i -e 's/include_directories(\${LIBXML2/#&/g' -e 's/include_directories(\${GLIB/#&/g' -e 's/include_directories(\${JSONC/#&/g' -e 's/include_directories(\${REPO/#&/g' -e 's/target_include_directories(/#&/g'
%global optflags %{optflags} -I%{_prefix}/%{_target_platform}/include/glib-2.0 -I%{_prefix}/%{_target_platform}/include/gio-unix-2.0 -I%{_prefix}/%{_target_platform}/%{_lib}/glib-2.0/include -I%{_prefix}/%{_target_platform}/include/libxml2 -I%{_prefix}/%{_target_platform}/include/json-c -Wno-error=vla-cxx-extension
%endif

%cmake \
	-G Ninja \
	-DWITH_PLUGIN_RHSM=OFF \
	-DWITH_MAN:BOOL=true \
	-DPERL_INSTALLDIRS=vendor \
%if %{with ruby}
	-DRuby_VENDORARCH_DIR=%{_libdir}/ruby/vendor_ruby/3.2.0 \
	-DRuby_VENDORLIBDIR=%{_datadir}/ruby/vendor_ruby \
%else
	-DWITH_RUBY:BOOL=OFF \
%endif
	-DPython3_EXECUTABLE=%{_bindir}/python \
	-DPERL_EXECUTABLE=%{_bindir}/perl \
	-DPKG_CONFIG_EXECUTABLE=%{_bindir}/pkg-config

%build
%ninja_build -C build
%ninja_build -C build doc-man

%install
%ninja_install -C build

# We don't need the README -- we know it's a plugin drop dir
rm %{buildroot}%{_prefix}/lib/python*/site-packages/libdnf_plugins/README

%if %{with dnf5_default}
ln -sr %{buildroot}%{_bindir}/dnf5 %{buildroot}%{_bindir}/dnf
ln -sr %{buildroot}%{_bindir}/dnf5 %{buildroot}%{_bindir}/yum
%endif

ln -sr %{buildroot}%{_bindir}/dnf5 %{buildroot}%{_bindir}/microdnf

# We get this from distro-release -- to make sure $releasever is set
# correctly and to share the file between dnf4 and dnf5
rm %{buildroot}%{_sysconfdir}/dnf/dnf.conf

%find_lang dnf5
%find_lang dnf5-plugin-automatic
%find_lang dnf5-plugin-builddep
%find_lang dnf5-plugin-changelog
%find_lang dnf5-plugin-config-manager
%find_lang dnf5-plugin-copr
%find_lang dnf5-plugin-needs-restarting
%find_lang dnf5-plugin-repoclosure
%find_lang dnf5-plugin-reposync
%find_lang dnf5daemon-client
%find_lang dnf5daemon-server
%find_lang libdnf5
%find_lang libdnf5-cli
%find_lang libdnf5-plugin-actions
%find_lang libdnf5-plugin-expired-pgp-keys

%post -n dnf5daemon-server
%systemd_post dnf5daemon-server.service

%preun -n dnf5daemon-server
%systemd_preun dnf5daemon-server.service

%postun -n dnf5daemon-server
%systemd_postun_with_restart dnf5daemon-server.service

%files -f dnf5.lang -f dnf5-plugin-builddep.lang -f dnf5-plugin-changelog.lang -f dnf5-plugin-config-manager.lang -f dnf5-plugin-copr.lang -f dnf5-plugin-needs-restarting.lang -f dnf5-plugin-repoclosure.lang -f libdnf5-plugin-actions.lang -f dnf5-plugin-reposync.lang
%dir %{_sysconfdir}/dnf
%dir %{_sysconfdir}/dnf/dnf5-aliases.d
%doc %{_sysconfdir}/dnf/dnf5-aliases.d/README
%dir %{_datadir}/dnf5
%dir %{_datadir}/dnf5/aliases.d
%dir %{_datadir}/dnf5/dnf5-plugins
%config %{_datadir}/dnf5/aliases.d/compatibility-plugins.conf
%config %{_datadir}/dnf5/aliases.d/compatibility-reposync.conf
%config %{_datadir}/dnf5/aliases.d/compatibility.conf
%{_bindir}/dnf5
%{_bindir}/microdnf
%if %{with dnf5_default}
%{_bindir}/dnf
%{_bindir}/yum
%endif
%{_datadir}/bash-completion/completions/dnf5
%{_libdir}/dnf5
%dir %{_datadir}/dnf5/libdnf.conf.d
%dir %{_sysconfdir}/dnf/libdnf5.conf.d
%dir %{_datadir}/dnf5/repos.override.d
%dir %{_sysconfdir}/dnf/repos.override.d
%dir %{_libdir}/libdnf5
%dir %{_libdir}/libdnf5/plugins
%{_libdir}/libdnf5/plugins/actions.so
%config %{_sysconfdir}/dnf/libdnf5-plugins/actions.conf
%dir %{_sysconfdir}/dnf/libdnf5-plugins/actions.d
%doc %{_mandir}/man5/dnf5.conf.5*
%doc %{_mandir}/man5/dnf5.conf-todo.5*
%doc %{_mandir}/man5/dnf5.conf-deprecated.5*
%doc %{_mandir}/man8/libdnf5-actions.8*
%doc %{_mandir}/man7/dnf5*.7*
%doc %{_mandir}/man8/dnf5.8*
%doc %{_mandir}/man8/dnf5-advisory.8*
%doc %{_mandir}/man8/dnf5-autoremove.8*
%doc %{_mandir}/man8/dnf5-builddep.8*
%doc %{_mandir}/man8/dnf5-check.8*
%doc %{_mandir}/man8/dnf5-clean.8*
%doc %{_mandir}/man8/dnf5-copr.8*
%doc %{_mandir}/man8/dnf5-distro-sync.8*
%doc %{_mandir}/man8/dnf5-downgrade.8*
%doc %{_mandir}/man8/dnf5-download.8*
%doc %{_mandir}/man8/dnf5-environment.8*
%doc %{_mandir}/man8/dnf5-group.8*
%doc %{_mandir}/man8/dnf5-history.8*
%doc %{_mandir}/man8/dnf5-install.8*
%doc %{_mandir}/man8/dnf5-leaves.8*
%doc %{_mandir}/man8/dnf5-makecache.8*
%doc %{_mandir}/man8/dnf5-mark.8*
%doc %{_mandir}/man8/dnf5-needs-restarting.8*
%doc %{_mandir}/man8/dnf5-provides.8*
%doc %{_mandir}/man8/dnf5-reinstall.8*
%doc %{_mandir}/man8/dnf5-remove.8*
%doc %{_mandir}/man8/dnf5-repo.8*
%doc %{_mandir}/man8/dnf5-repoclosure.8*
%doc %{_mandir}/man8/dnf5-repoquery.8*
%doc %{_mandir}/man8/dnf5-reposync.8*
%doc %{_mandir}/man8/dnf5-search.8*
%doc %{_mandir}/man8/dnf5-swap.8*
%doc %{_mandir}/man8/dnf5-upgrade.8*
%doc %{_mandir}/man8/dnf5-changelog.8*
%doc %{_mandir}/man8/dnf5-check-upgrade.8*
%doc %{_mandir}/man8/dnf5-info.8*
%doc %{_mandir}/man8/dnf5-list.8*
%doc %{_mandir}/man8/dnf5-module.8*
%doc %{_mandir}/man8/dnf5-offline.8*
%doc %{_mandir}/man8/dnf5-system-upgrade.8*
%doc %{_mandir}/man8/dnf5-versionlock.8*
%doc %{_mandir}/man8/dnf5-config-manager.8.zst
%doc %{_mandir}/man8/dnf5-replay.8*


%files plugin-automatic -f dnf5-plugin-automatic.lang
%{_bindir}/dnf-automatic
%{_prefix}/lib/systemd/system/dnf-automatic.service
%{_prefix}/lib/systemd/system/dnf-automatic.timer
%{_prefix}/lib/systemd/system/dnf5-automatic.service
%{_prefix}/lib/systemd/system/dnf5-automatic.timer
%{_prefix}/lib/systemd/system/dnf5-makecache.service
%{_prefix}/lib/systemd/system/dnf5-makecache.timer
%{_prefix}/lib/systemd/system/dnf5-offline-transaction-cleanup.service
%{_prefix}/lib/systemd/system/dnf5-offline-transaction.service
%{_datadir}/dnf5/dnf5-plugins/automatic.conf
%doc %{_mandir}/man8/dnf5-automatic.8*

%files plugin-appstream
%config %{_sysconfdir}/dnf/libdnf5-plugins/appstream.conf
%{_libdir}/libdnf5/plugins/appstream.so

%files plugin-expired-pgp-keys -f libdnf5-plugin-expired-pgp-keys.lang
%config %{_sysconfdir}/dnf/libdnf5-plugins/expired-pgp-keys.conf
%{_libdir}/libdnf5/plugins/expired-pgp-keys.so
%{_mandir}/man8/libdnf5-expired-pgp-keys.8*

%files -n %{libname} -f libdnf5.lang
%if %{with dnf5_default}
%dir %{_sysconfdir}/dnf/vars
%dir %{_sysconfdir}/dnf/protected.d
%endif
%dir %{_sysconfdir}/dnf/libdnf5-plugins
%dir %{_libdir}/libdnf5
%{_libdir}/libdnf5.so.%{major}*

%files -n %{clilibname} -f libdnf5-cli.lang
%{_libdir}/libdnf5-cli.so.%{major}*

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
%dir %{python_sitelib}/libdnf_plugins/
%{_libdir}/libdnf5/plugins/python_plugins_loader.*
%{python_sitearch}/libdnf5
%{python_sitearch}/libdnf5-*.dist-info
%{python_sitearch}/libdnf5_cli
%{python_sitearch}/libdnf5_cli-*.dist-info

%files -n perl-%{name}
%{_libdir}/perl5/vendor_perl/auto/libdnf5
%{_libdir}/perl5/vendor_perl/auto/libdnf5_cli
%{_libdir}/perl5/vendor_perl/libdnf5
%{_libdir}/perl5/vendor_perl/libdnf5_cli

%if %{with ruby}
%files -n ruby-%{name}
%{_libdir}/ruby/vendor_ruby/*/*
%endif
