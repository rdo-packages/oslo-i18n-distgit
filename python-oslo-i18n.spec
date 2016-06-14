%global pypi_name oslo.i18n

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-oslo-i18n
Version:        XXX
Release:        XXX
Summary:        OpenStack i18n library
License:        ASL 2.0
URL:            https://github.com/openstack/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%description
The oslo.i18n library contain utilities for working with internationalization
(i18n) features, especially translation for text strings in an application
or library.

%package -n python2-oslo-i18n
Summary:        OpenStack i18n Python 2 library
%{?python_provide:%python_provide python2-oslo-i18n}
# python_provide does not exist in CBS Cloud buildroot
Provides:       python-oslo-i18n = %{version}-%{release}
Obsoletes:      python-oslo-i18n < 2.5.0-2

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
# python_provide does not exist in CBS Cloud buildroot
Provides:       python-oslo-i18n-doc = %{version}-%{release}
Obsoletes:      python-oslo-i18n-doc < 2.5.0-2

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
%setup -qc
mv %{pypi_name}-%{upstream_version} python2

pushd python2
rm -rf *.egg-info

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

cp -p LICENSE ChangeLog CONTRIBUTING.rst PKG-INFO README.rst ../
popd

find python2 -name '*.py' | xargs sed -i 's|^#!python|#!%{__python2}|'

%if 0%{?with_python3}
cp -a python2 python3
find python3 -name '*.py' | xargs sed -i 's|^#!python|#!%{__python3}|'
%endif

%build
pushd python2
%{__python2} setup.py build
popd
%if 0%{?with_python3}
pushd python3
%{__python3} setup.py build
popd
%endif

%install
pushd python2
%{__python2} setup.py install --skip-build --root %{buildroot}
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.buildinfo

# Fix this rpmlint warning
sed -i "s|\r||g" build/html/_static/jquery.js
popd
popd

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
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
%doc python2/doc/build/html

%if 0%{?with_python3}
%files -n python3-oslo-i18n-doc
%license LICENSE
%doc python3/doc/build/html
%endif

%changelog
