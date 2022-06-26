%define snapshot 20220624

Name: dnf5
Version: 0.67.1
Release: %{?snapshot:0.%{snapshot}.}1
Source0: https://github.com/rpm-software-management/libdnf/archive/refs/heads/dnf-5-devel.tar.gz#/dnf5-%{snapshot}.tar.gz
Patch0: https://github.com/rpm-software-management/libdnf/pull/1551.patch
Summary: Upcoming version of the DNF package manager
URL: https://github.com/rpm-software-management/libdnf/tree/dnf-5-devel
License: GPL
Group: System/Configuration/Packaging
BuildRequires: cmake ninja
BuildRequires: cmake(toml11)
BuildRequires: perl(Test::Exception)
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
# Language bindings
BuildRequires: perl-devel
BuildRequires: pkgconfig(python3)
BuildRequires: ruby-devel
BuildRequires: swig
# For building man pages
BuildRequires: python-sphinx
BuildRequires: python3dist(breathe)

%description
Upcoming version of the DNF package manager

%define libname %mklibname dnf
%define clilibname %mklibname dnf-cli
%define devname %mklibname -d dnf

%package -n %{libname}
Summary: DNF 5 library
Group: System/Libraries

%description -n %{libname}
DNF 5 library

%package -n %{clilibname}
Summary: DNF 5 CLI library
Group: System/Libraries

%description -n %{clilibname}
DNF 5 CLI library

%package -n %{devname}
Summary: Development files for the DNF package management library
Group: Development/C++ and C
Requires: %{libname} = %{EVRD}
Requires: %{clilibname} = %{EVRD}

%description -n %{devname}
Development files for the DNF package management library

%package -n python-%{name}
Summary: Python language bindings to the DNF package manager
Group: Development/Python

%description -n python-%{name}
Python language bindings to the DNF package manager

%package -n perl-%{name}
Summary: Perl language bindings to the DNF package manager
Group: Development/Perl

%description -n perl-%{name}
Perl language bindings to the DNF package manager

%package -n ruby-%{name}
Summary: Ruby language bindings to the DNF package manager
Group: Development/Ruby

%description -n ruby-%{name}
Ruby language bindings to the DNF package manager

%prep
%autosetup -p1 -n libdnf-dnf-5-devel
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

%files
%{_sysconfdir}/dbus-1/system.d/org.rpm.dnf.v0.conf
%{_bindir}/dnf5
%{_bindir}/dnf5daemon-client
%{_bindir}/dnf5daemon-server
%{_datadir}/bash-completion/completions/dnf5
%{_datadir}/dbus-1/interfaces/org.rpm.dnf.v0.Goal.xml
%{_datadir}/dbus-1/interfaces/org.rpm.dnf.v0.SessionManager.xml
%{_datadir}/dbus-1/interfaces/org.rpm.dnf.v0.rpm.Repo.xml
%{_datadir}/dbus-1/interfaces/org.rpm.dnf.v0.rpm.Rpm.xml
%{_datadir}/dbus-1/system-services/org.rpm.dnf.v0.service
%{_datadir}/polkit-1/actions/org.rpm.dnf.v0.policy
%{_prefix}/lib/systemd/system/dnf5daemon-server.service
%{_libdir}/dnf5
%{_libdir}/libdnf-plugins
%doc %{_mandir}/man8/dnf5.8*
%doc %{_mandir}/man8/dnf5daemon-client.8*
%doc %{_mandir}/man8/dnf5daemon-dbus-api.8*
%doc %{_mandir}/man8/dnf5daemon-server.8*

%files -n %{libname}
%{_libdir}/libdnf.so.3*

%files -n %{clilibname}
%{_libdir}/libdnf-cli.so.0*

%files -n %{devname}
%{_includedir}/libdnf-cli
%{_includedir}/libdnf
%{_libdir}/libdnf-cli.so
%{_libdir}/libdnf.so
%{_libdir}/pkgconfig/libdnf.pc
%{_libdir}/pkgconfig/libdnf-cli.pc

%files -n python-%{name}
%{_prefix}/lib/python*/site-packages/libdnf_plugins
%{_libdir}/python*/site-packages/libdnf
%{_libdir}/python*/site-packages/libdnf_cli

%files -n perl-%{name}
%{_libdir}/perl5/vendor_perl/auto/libdnf
%{_libdir}/perl5/vendor_perl/auto/libdnf_cli
%{_libdir}/perl5/vendor_perl/libdnf
%{_libdir}/perl5/vendor_perl/libdnf_cli

%files -n ruby-%{name}
%{_libdir}/ruby/vendor_ruby/*/*
