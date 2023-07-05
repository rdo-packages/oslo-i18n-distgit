%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

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
License:        Apache-2.0
URL:            https://github.com/openstack/%{pypi_name}
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python3-%{pkg_name}
Summary:        OpenStack i18n Python 2 library

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:        Documentation for OpenStack i18n library

%description -n python-%{pkg_name}-doc
Documentation for the oslo.i18n library.
%endif

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo i18n library

%description -n python-%{pkg_name}-lang
Translation files for Oslo i18n library

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_doc}
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

# Generate i18n files
python3 setup.py compile_catalog -d %{buildroot}%{python3_sitelib}/oslo_i18n/locale --domain oslo_i18n

# Fix this rpmlint warning
if [ -f html/_static/jquery.js ]; then
sed -i "s|\r||g" html/_static/jquery.js
fi
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
%{python3_sitelib}/*.dist-info

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python-%{pkg_name}-lang -f oslo_i18n.lang
%license LICENSE

%changelog
