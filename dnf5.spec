#define snapshot 20220923
%define major 1
%define libname %mklibname dnf %{major}
%define clilibname %mklibname dnf-cli
%define devname %mklibname -d dnf

Summary: Command-line package manager
Name: dnf5
Version: 5.0.0
Release: %{?snapshot:0.%{snapshot}.}3
URL: https://github.com/rpm-software-management/dnf5
License: GPL
Group: System/Configuration/Packaging
%if 0%{?snapshot:1}
Source0: https://github.com/rpm-software-management/dnf5/archive/refs/heads/main.tar.gz#/dnf5-%{snapshot}.tar.gz
%else
Source0: https://github.com/rpm-software-management/dnf5/archive/refs/tags/%{name}-%{version}.tar.gz
%endif
Patch0: dnf5-znver1.patch
Patch1: https://github.com/rpm-software-management/dnf5/pull/111.patch
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: cmake(toml11)
BuildRequires: perl(Test::Exception)
BuildRequires: pkgconfig(libcomps)
BuildRequires: pkgconfig(fmt)
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(modulemd-2.0)
BuildRequires: pkgconfig(libsolv)
BuildRequires: pkgconfig(libsolvext)
BuildRequires: pkgconfig(rpm)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(zck)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gpgme)
BuildRequires: pkgconfig(librepo)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(smartcols)
BuildRequires: pkgconfig(sdbus-c++)
BuildRequires: pkgconfig(cppunit)
BuildRequires: cmake(bash-completion)
BuildRequires: createrepo_c
# For -lstdc++fs, but is that really needed?
BuildRequires: stdc++-static-devel
# Language bindings
BuildRequires: perl-devel
BuildRequires: pkgconfig(python3)
BuildRequires: ruby-devel
BuildRequires: swig
# For building man pages
BuildRequires: python-sphinx
BuildRequires: python3dist(breathe)
Requires: dnf-data
Recommends: bash-completion

%description
DNF5 is a command-line package manager that automates the process of installing,
upgrading, configuring, and removing computer programs in a consistent manner.
It supports RPM packages, modulemd modules, and comps groups & environments.

%package -n %{libname}
Summary: DNF 5 library
Group: System/Libraries

%description -n %{libname}
DNF 5 library.

%package -n %{clilibname}
Summary: DNF 5 CLI library
Group: System/Libraries

%description -n %{clilibname}
DNF 5 CLI library.

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
Requires: dnf-data

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
%cmake \
	-G Ninja \
	-DWITH_MAN:BOOL=true \
	-DPERL_INSTALLDIRS=vendor \
	-DRuby_VENDORARCH_DIR=%{_libdir}/ruby/vendor_ruby/2.7.0 \
	-DRuby_VENDORLIBDIR=%{_datadir}/ruby/vendor_ruby

%build
%ninja_build -C build
%ninja_build -C build doc-man

%install
%ninja_install -C build
# We don't need the README -- we know it's a plugin drop dir
rm %{buildroot}%{_prefix}/lib/python*/site-packages/libdnf_plugins/README

%post -n dnf5daemon-server
%systemd_post dnf5daemon-server.service

%preun -n dnf5daemon-server
%systemd_preun dnf5daemon-server.service

%postun -n dnf5daemon-server
%systemd_postun_with_restart dnf5daemon-server.service

%files
%dir %{_sysconfdir}/dnf
%dir %{_sysconfdir}/dnf/dnf5-aliases.d
%doc %{_sysconfdir}/dnf/dnf5-aliases.d/README
%dir %{_prefix}/lib/dnf5
%dir %{_prefix}/lib/dnf5/aliases.d
%config %{_prefix}/lib/dnf5/aliases.d/compatibility.conf
%{_bindir}/dnf5
%{_datadir}/bash-completion/completions/dnf5
%{_libdir}/dnf5
%dir %{_libdir}/libdnf5
%dir %{_libdir}/libdnf5/plugins
%{_libdir}/libdnf5/plugins/actions.so
%doc %{_mandir}/man8/dnf5.8*

%files -n %{libname}
%{_libdir}/libdnf5.so.%{major}*
%{_var}/cache/libdnf/

%files -n %{clilibname}
%{_libdir}/libdnf-cli.so.%{major}*

%files -n dnf5daemon-client
%{_bindir}/dnf5daemon-client
%doc %{_mandir}/man8/dnf5daemon-client.8.*

%files -n dnf5daemon-server
%{_bindir}/dnf5daemon-server
%{_unitdir}/dnf5daemon-server.service
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.rpm.dnf.v0.conf
%{_datadir}/dbus-1/system-services/org.rpm.dnf.v0.service
%{_datadir}/dbus-1/interfaces/org.rpm.dnf.v0.*.xml
%{_datadir}/polkit-1/actions/org.rpm.dnf.v0.policy
%doc %{_mandir}/man8/dnf5daemon-server.8.*
%doc %{_mandir}/man8/dnf5daemon-dbus-api.8.*

%files -n %{devname}
%{_includedir}/libdnf-cli
%{_includedir}/libdnf
%{_libdir}/libdnf-cli.so
%{_libdir}/libdnf5.so
%{_libdir}/pkgconfig/libdnf.pc
%{_libdir}/pkgconfig/libdnf-cli.pc

%files -n python-%{name}
%{_libdir}/libdnf5/plugins/python_plugins_loader.so
%dir %{_prefix}/lib/python*/site-packages/libdnf_plugins
%{_libdir}/python*/site-packages/libdnf5
%{_libdir}/python*/site-packages/libdnf5_cli

%files -n perl-%{name}
%{_libdir}/perl5/vendor_perl/auto/libdnf5
%{_libdir}/perl5/vendor_perl/auto/libdnf5_cli
%{_libdir}/perl5/vendor_perl/libdnf5
%{_libdir}/perl5/vendor_perl/libdnf5_cli

%files -n ruby-%{name}
%{_libdir}/ruby/vendor_ruby/*/*
