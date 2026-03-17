%global package_speccommit 8951d5ced6bb27c830ac30bd77d97de8c3970191
%global usver 2.4.3
%global xsver 1
%global xsrel %{xsver}%{?xscount}%{?xshash}
%bcond_without python3

Name: libtalloc
Version: 2.4.3
Release: %{?xsrel}.1%{?dist}
Summary:         The talloc library
License:         LGPL-3.0-or-later
URL:             https://talloc.samba.org/

Source0: talloc-2.4.3.tar.gz

BuildRequires: make
BuildRequires: gcc
BuildRequires: libxslt
BuildRequires: python3-devel
BuildRequires: gnupg2

Provides: bundled(libreplace)

# Python bindings no more used by system:
# Samba does not build runtime python libraries anymore
# XS removal of a version XCP-ng did not ship
Obsoletes: python2-talloc < 2.2.0-1
Obsoletes: python2-talloc-devel < 2.2.0-1
# XCP-ng: Removal of a previous samba requirement
Obsoletes: pytalloc <= 2.1.16-1.el7
Obsoletes: pytalloc-devel <= 2.1.16-1.el7

%description
A library that implements a hierarchical allocator with destructors.

%package devel
Summary:         Developer tools for the Talloc library

Requires: libtalloc = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Talloc library.

%if %{with python3}
%package -n python3-talloc
Summary:         Python bindings for the Talloc library

Requires: libtalloc = %{version}-%{release}
%{?python_provide:%python_provide python3-talloc}

%description -n python3-talloc
Python 3 libraries for creating bindings using talloc

%package -n python3-talloc-devel
Summary:         Development libraries for python3-talloc

Requires: python3-talloc = %{version}-%{release}
%{?python_provide:%python_provide python3-talloc-devel}

%description -n python3-talloc-devel
Development libraries for python3-talloc
%endif

%prep
%autosetup -n talloc-%{version} -p1

%build
# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1217376
export python_LDFLAGS=""

%configure --disable-rpath \
           --disable-rpath-install \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules

%make_build

%check
%make_build check

%install
%make_install

%files
%license LICENSE
%{_libdir}/libtalloc.so.*

%files devel
%{_includedir}/talloc.h
%{_libdir}/libtalloc.so
%{_libdir}/pkgconfig/talloc.pc

%if %{with python3}
%files -n python3-talloc
%{_libdir}/libpytalloc-util.cpython*.so.*
%{python3_sitearch}/talloc.cpython*.so

%files -n python3-talloc-devel
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.cpython-*.pc
%{_libdir}/libpytalloc-util.cpython*.so
%endif

%ldconfig_scriptlets

%if %{with python3}
%ldconfig_scriptlets -n python3-talloc
%endif

%changelog
* Wed Jul 15 2026 Philippe Coval <philippe.coval@vates.tech> - 2.4.3-1.1
- Obsoletes pytalloc

* Fri Sep 19 2025 Lin Liu <lin.liu@citrix.com> - 2.4.3-1
- CP-310101: Update to 2.4.3 for samba update

* Tue Jan 21 2025 XenServer Rebuild <rebuild@xenserver.com> - 2.4.0-2
- CP-53310: XenServer 9 rebuild

* Mon Dec 11 2023 Lin Liu <lin.liu@citrix.com> - 2.4.0-1
- Update to 2.4.0 to build samba

* Wed Jul 05 2023 Lin Liu <lin.liu@citrix.com> - 2.3.4-1
- First imported release

