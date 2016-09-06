%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name oslo.i18n
%global pkg_name oslo-i18n

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-oslo-i18n
Version:        3.5.0
Release:        1%{?dist}
Summary:        OpenStack i18n library
License:        ASL 2.0
URL:            https://github.com/openstack/%{pypi_name}
Source0:        https://pypi.io/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

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

Requires:       python-setuptools
Requires:       python-babel
Requires:       python-six
Requires:       python-fixtures

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

Requires:       python3-setuptools
Requires:       python3-babel
Requires:       python3-six
Requires:       python3-fixtures

%description -n python3-oslo-i18n
The oslo.i18n library contain utilities for working with internationalization
(i18n) features, especially translation for text strings in an application
or library.
%endif

%package -n python2-oslo-i18n-doc
Summary:        Documentation for OpenStack i18n library
%{?python_provide:%python_provide python2-oslo-i18n-doc}

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description -n python2-oslo-i18n-doc
Documentation for the oslo.i18n library.

%if 0%{?with_python3}
%package -n python3-oslo-i18n-doc
Summary:        Documentation for OpenStack i18n library
%{?python_provide:%python_provide python3-oslo-i18n-doc}

BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx

%description -n python3-oslo-i18n-doc
Documentation for the oslo.i18n library.
%endif

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

%install
%py2_install
sphinx-build -b html doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

# Fix this rpmlint warning
sed -i "s|\r||g" html/_static/jquery.js

%if 0%{?with_python3}
%py3_install
%endif

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

%files -n python2-oslo-i18n-doc
%license LICENSE
%doc html

%if 0%{?with_python3}
%files -n python3-oslo-i18n-doc
%license LICENSE
%doc html
%endif

%changelog
* Tue Sep 06 2016 Haikel Guemar <hguemar@fedoraproject.org> 3.5.0-1
- Update to 3.5.0

* Tue Mar 22 2016 Haikel Guemar <hguemar@fedoraproject.org> 3.4.0-
- Update to 3.4.0

