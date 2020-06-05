%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name oslo.i18n
%global pkg_name oslo-i18n
%global with_doc 1

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

%package -n python3-%{pkg_name}
Summary:        OpenStack i18n Python 2 library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-babel
BuildRequires:  python3-six
BuildRequires:  python3-fixtures
# Required to compile translation files
BuildRequires:  python3-babel

Requires:       python3-babel
Requires:       python3-six
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:        Documentation for OpenStack i18n library

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinxcontrib-apidoc

%description -n python-%{pkg_name}-doc
Documentation for the oslo.i18n library.
%endif

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
%{py3_build}

# Generate i18n files
python3 setup.py compile_catalog -d build/lib/oslo_i18n/locale --domain oslo_i18n

%install
%{py3_install}

%if 0%{?with_doc}
python3 setup.py build_sphinx --build-dir . -b html
# remove the sphinx-build-3 leftovers
rm -rf html/.{doctrees,buildinfo}

# Fix this rpmlint warning
sed -i "s|\r||g" html/_static/jquery.js
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_i18n/locale/*/LC_*/oslo_i18n*po
rm -f %{buildroot}%{python3_sitelib}/oslo_i18n/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_i18n/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_i18n --all-name

%files -n python3-%{pkg_name}
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{python3_sitelib}/oslo_i18n
%{python3_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%license LICENSE
%doc html
%endif

%files -n python-%{pkg_name}-lang -f oslo_i18n.lang
%license LICENSE

%changelog
