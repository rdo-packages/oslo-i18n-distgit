%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name oslo.i18n
%global pkg_name oslo-i18n

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-oslo-i18n
Version:        XXX
Release:        XXX
Summary:        OpenStack i18n library
License:        ASL 2.0
URL:            https://github.com/openstack/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{uptream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git

%description
The oslo.i18n library contain utilities for working with internationalization
(i18n) features, especially translation for text strings in an application
or library.

%package -n python2-oslo-i18n
Summary:        OpenStack i18n Python 2 library
%{?python_provide:%python_provide python2-oslo-i18n}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  python-babel
BuildRequires:  python-six
BuildRequires:  python-fixtures
# Required to compile translation files
BuildRequires:  python-babel

Requires:       python-babel
Requires:       python-six
Requires:       python-fixtures
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python2-oslo-i18n
The oslo.i18n library contain utilities for working with internationalization
(i18n) features, especially translation for text strings in an application
or library.

%if 0%{?with_python3}
%package -n python3-oslo-i18n
Summary:        OpenStack i18n Python 3 library
%{?python_provide:%python_provide python3-oslo-i18n}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-babel
BuildRequires:  python3-six
BuildRequires:  python3-fixtures

Requires:       python3-babel
Requires:       python3-six
Requires:       python3-fixtures
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-oslo-i18n
The oslo.i18n library contain utilities for working with internationalization
(i18n) features, especially translation for text strings in an application
or library.
%endif

%package -n python-oslo-i18n-doc
Summary:        Documentation for OpenStack i18n library

Provides:  python2-oslo-i18n-doc = %{version}-%{release}
Provides:  python3-oslo-i18n-doc = %{version}-%{release}
Obsoletes: python2-oslo-i18n-doc <= 3.9.0-1
Obsoletes: python3-oslo-i18n-doc <= 3.9.0-1

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme

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
rm -f test-requirements.txt requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/oslo_i18n/locale

%install
%py2_install
%{__python2} setup.py build_sphinx --build-dir . -b html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

# Fix this rpmlint warning
sed -i "s|\r||g" html/_static/jquery.js

%if 0%{?with_python3}
%py3_install
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/oslo_i18n/locale/*/LC_*/oslo_i18n*po
rm -f %{buildroot}%{python2_sitelib}/oslo_i18n/locale/*pot
mv %{buildroot}%{python2_sitelib}/oslo_i18n/locale %{buildroot}%{_datadir}/locale
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/oslo_i18n/locale
%endif

# Find language files
%find_lang oslo_i18n --all-name

%files -n python2-oslo-i18n
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{python2_sitelib}/oslo_i18n
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-oslo-i18n
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{python3_sitelib}/oslo_i18n
%{python3_sitelib}/*.egg-info
%endif

%files -n python-oslo-i18n-doc
%license LICENSE
%doc html

%files -n python-%{pkg_name}-lang -f oslo_i18n.lang
%license LICENSE

%changelog
