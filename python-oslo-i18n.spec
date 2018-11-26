# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name oslo.i18n
%global pkg_name oslo-i18n

%global common_desc \
The oslo.i18n library contain utilities for working with internationalization \
(i18n) features, especially translation for text strings in an application \
or library.

Name:           python-oslo-i18n
Version:        XXX
Release:        XXX
Summary:        OpenStack i18n library
License:        ASL 2.0
URL:            https://github.com/openstack/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-oslo-i18n
Summary:        OpenStack i18n Python 2 library
%{?python_provide:%python_provide python%{pyver}-oslo-i18n}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-babel
BuildRequires:  python%{pyver}-six
BuildRequires:  python%{pyver}-fixtures
# Required to compile translation files
BuildRequires:  python%{pyver}-babel

Requires:       python%{pyver}-babel
Requires:       python%{pyver}-six
Requires:       python%{pyver}-fixtures
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python%{pyver}-oslo-i18n
%{common_desc}

%package -n python-oslo-i18n-doc
Summary:        Documentation for OpenStack i18n library

Provides:  python%{pyver}-oslo-i18n-doc = %{version}-%{release}
Obsoletes: python%{pyver}-oslo-i18n-doc <= 3.9.0-1

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

%description -n python-oslo-i18n-doc
Documentation for the oslo.i18n library.

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo i18n library

%description -n python-%{pkg_name}-lang
Translation files for Oslo i18n library

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
rm -rf *.egg-info

# Let RPM handle the dependencies
%py_req_cleanup

%build
%{pyver_build}

# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/oslo_i18n/locale

%install
%{pyver_install}

%{pyver_bin} setup.py build_sphinx --build-dir . -b html
# remove the sphinx-build-%{pyver} leftovers
rm -rf html/.{doctrees,buildinfo}

# Fix this rpmlint warning
sed -i "s|\r||g" html/_static/jquery.js

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/oslo_i18n/locale/*/LC_*/oslo_i18n*po
rm -f %{buildroot}%{pyver_sitelib}/oslo_i18n/locale/*pot
mv %{buildroot}%{pyver_sitelib}/oslo_i18n/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_i18n --all-name

%files -n python%{pyver}-oslo-i18n
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{pyver_sitelib}/oslo_i18n
%{pyver_sitelib}/*.egg-info

%files -n python-oslo-i18n-doc
%license LICENSE
%doc html

%files -n python-%{pkg_name}-lang -f oslo_i18n.lang
%license LICENSE

%changelog
