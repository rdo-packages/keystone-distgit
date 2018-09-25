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

%global with_doc 1
%global service keystone
# guard for package OSP does not support
%global rhosp 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Keystone is a Python implementation of the OpenStack \
(http://www.openstack.org) identity service API.

Name:           openstack-keystone
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:          1
Version:        XXX
Release:        XXX
Summary:        OpenStack Identity Service
License:        ASL 2.0
URL:            http://keystone.openstack.org/
Source0:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
Source1:        openstack-keystone.logrotate
Source3:        openstack-keystone.sysctl
Source5:        openstack-keystone-sample-data
Source20:       keystone-dist.conf

BuildArch:      noarch
BuildRequires:  openstack-macros
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-osprofiler >= 1.1.0
BuildRequires:  python%{pyver}-pbr >= 1.8
BuildRequires:  git
# Required to build keystone.conf
BuildRequires:  python%{pyver}-oslo-cache >= 1.26.0
BuildRequires:  python%{pyver}-oslo-config >= 2:5.2.0
BuildRequires:  python%{pyver}-passlib >= 1.6
BuildRequires:  python%{pyver}-pycadf >= 2.1.0
# Required to compile translation files
BuildRequires:  python%{pyver}-babel
# Required to build man pages
BuildRequires:  python%{pyver}-oslo-policy
BuildRequires:  python%{pyver}-jsonschema
BuildRequires:  python%{pyver}-oslo-db >= 4.27.0
BuildRequires:  python%{pyver}-pysaml2
BuildRequires:  python%{pyver}-keystonemiddleware >= 4.17.0
BuildRequires:  python%{pyver}-testresources
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-oslotest
# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-oauthlib
BuildRequires:  python-redis
%if 0%{rhosp} == 0
BuildRequires:  python-zmq
%endif
BuildRequires:  python-ldappool
BuildRequires:  python-webtest
BuildRequires:  python-freezegun
BuildRequires:  python-pep8
%else
BuildRequires:  python%{pyver}-oauthlib
BuildRequires:  python%{pyver}-redis
%if 0%{rhosp} == 0
BuildRequires:  python%{pyver}-zmq
%endif
BuildRequires:  python%{pyver}-ldappool
BuildRequires:  python%{pyver}-webtest
BuildRequires:  python%{pyver}-freezegun
BuildRequires:  python%{pyver}-pep8
%endif

Requires:       python%{pyver}-keystone = %{epoch}:%{version}-%{release}
Requires:       python%{pyver}-keystoneclient >= 1:3.8.0

%{?systemd_requires}
BuildRequires: systemd
Requires(pre):    shadow-utils

%description
%{common_desc}

This package contains the Keystone daemon.

%package -n       python%{pyver}-keystone
Summary:          Keystone Python libraries
%{?python_provide:%python_provide python%{pyver}-keystone}

Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-bcrypt
Requires:       python%{pyver}-routes >= 2.3.1
Requires:       python%{pyver}-sqlalchemy >= 1.0.10
Requires:       python%{pyver}-passlib >= 1.7.0
Requires:       openssl
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-babel >= 2.3.4
Requires:       python%{pyver}-oauthlib >= 0.6.2
Requires:       python%{pyver}-jsonschema
Requires:       python%{pyver}-pycadf >= 2.1.0
Requires:       python%{pyver}-keystonemiddleware >= 4.17.0
Requires:       python%{pyver}-oslo-cache >= 1.26.0
Requires:       python%{pyver}-oslo-concurrency >= 3.26.0
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-context >= 2.21.0
Requires:       python%{pyver}-oslo-db >= 4.27.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-log >= 3.37.0
Requires:       python%{pyver}-oslo-messaging >= 5.29.0
Requires:       python%{pyver}-oslo-middleware >= 3.31.0
Requires:       python%{pyver}-oslo-policy >= 1.30.0
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-osprofiler >= 1.4.0
Requires:       python%{pyver}-pysaml2 >= 4.5.0
Requires:       python%{pyver}-stevedore >= 1.20.0
Requires:       python%{pyver}-scrypt
Requires:       python%{pyver}-flask
Requires:       python%{pyver}-flask-restful
# for Keystone Lightweight Tokens (KLWT)
Requires:       python%{pyver}-cryptography
# Handle python2 exception
%if %{pyver} == 2
Requires:       python-ldap
Requires:       python-ldappool
Requires:       python-memcached
Requires:       python-migrate >= 0.11.0
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-paste
Requires:       python-webob >= 1.7.1
Requires:       python-dogpile-cache >= 0.6.2
Requires:       python-msgpack
%else
Requires:       python%{pyver}-ldap
Requires:       python%{pyver}-ldappool
Requires:       python%{pyver}-memcached
Requires:       python%{pyver}-migrate >= 0.11.0
Requires:       python%{pyver}-paste-deploy >= 1.5.0
Requires:       python%{pyver}-paste
Requires:       python%{pyver}-webob >= 1.7.1
Requires:       python%{pyver}-dogpile-cache >= 0.6.2
Requires:       python%{pyver}-msgpack
%endif


%description -n   python%{pyver}-keystone
%{common_desc}

This package contains the Keystone Python library.

%package -n python%{pyver}-%{service}-tests
Summary:        Keystone tests
%{?python_provide:%python_provide python%{pyver}-%{service}-tests}
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

# Adding python-keystone-tests-tempest as Requires to keep backward
# compatibilty
%if %{pyver} == 2
Requires:       python%{pyver}-keystone-tests-tempest
%endif

%description -n python%{pyver}-%{service}-tests
%{common_desc}

This package contains the Keystone test files.


%if 0%{?with_doc}
%package doc
Summary:        Documentation for OpenStack Identity Service

# for API autodoc
BuildRequires:  python%{pyver}-sphinx >= 1.1.2
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinxcontrib-apidoc
BuildRequires:  python%{pyver}-flask
BuildRequires:  python%{pyver}-flask-restful
BuildRequires:  python%{pyver}-cryptography
BuildRequires:  python%{pyver}-oslo-concurrency >= 3.26.0
BuildRequires:  python%{pyver}-oslo-log >= 3.37.0
BuildRequires:  python%{pyver}-oslo-messaging >= 5.29.0
BuildRequires:  python%{pyver}-oslo-middleware >= 3.31.0
BuildRequires:  python%{pyver}-oslo-policy >= 1.30.0
BuildRequires:  python%{pyver}-routes
BuildRequires:  python%{pyver}-mock
# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-dogpile-cache >= 0.5.7
BuildRequires:  python-memcached
BuildRequires:  python-paste-deploy
BuildRequires:  python-lxml
%else
BuildRequires:  python%{pyver}-dogpile-cache >= 0.5.7
BuildRequires:  python%{pyver}-memcached
BuildRequires:  python%{pyver}-paste-deploy
BuildRequires:  python%{pyver}-lxml
%endif


%description doc
%{common_desc}

This package contains documentation for Keystone.
%endif

%prep
%autosetup -n keystone-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete
find keystone -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;
# Let RPM handle the dependencies
%py_req_cleanup

# adjust paths to WSGI scripts
sed -i 's#/local/bin#/bin#' httpd/wsgi-keystone.conf
sed -i 's#apache2#httpd#' httpd/wsgi-keystone.conf

%build
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=config-generator/keystone.conf
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=config-generator/keystone.conf --format yaml --output-file=%{service}-schema.yaml
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=config-generator/keystone.conf --format json --output-file=%{service}-schema.json
# distribution defaults are located in keystone-dist.conf

%{pyver_build}
# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/%{service}/locale -D keystone

%install
%{pyver_install}

# Keystone doesn't ship policy.json file but only an example
# that contains data which might be problematic to use by default.
# Instead, ship an empty file that operators can override.
echo "{}" > policy.json

install -d -m 755 %{buildroot}%{_sysconfdir}/keystone
install -p -D -m 640 etc/keystone.conf.sample %{buildroot}%{_sysconfdir}/keystone/keystone.conf
install -p -D -m 640 etc/keystone-paste.ini %{buildroot}%{_sysconfdir}/keystone/keystone-paste.ini
install -p -D -m 640 policy.json %{buildroot}%{_sysconfdir}/keystone/policy.json
install -p -D -m 640 %{service}-schema.yaml %{buildroot}%{_datadir}/%{service}/%{service}-schema.yaml
install -p -D -m 640 %{service}-schema.json %{buildroot}%{_datadir}/%{service}/%{service}-schema.json
install -p -D -m 644 %{SOURCE20} %{buildroot}%{_datadir}/keystone/keystone-dist.conf
install -p -D -m 644 etc/policy.v3cloudsample.json %{buildroot}%{_datadir}/keystone/policy.v3cloudsample.json
install -p -D -m 640 etc/logging.conf.sample %{buildroot}%{_sysconfdir}/keystone/logging.conf
install -p -D -m 640 etc/default_catalog.templates %{buildroot}%{_sysconfdir}/keystone/default_catalog.templates
install -p -D -m 640 etc/sso_callback_template.html %{buildroot}%{_sysconfdir}/keystone/sso_callback_template.html
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-keystone
install -d -m 755 %{buildroot}%{_prefix}/lib/sysctl.d
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_prefix}/lib/sysctl.d/openstack-keystone.conf
# Install sample data script.
install -p -D -m 755 tools/sample_data.sh %{buildroot}%{_datadir}/keystone/sample_data.sh
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_bindir}/openstack-keystone-sample-data
# Install sample HTTPD integration files
install -p -D -m 644 httpd/wsgi-keystone.conf  %{buildroot}%{_datadir}/keystone/

install -d -m 755 %{buildroot}%{_sharedstatedir}/keystone
install -d -m 755 %{buildroot}%{_localstatedir}/log/keystone

# cleanup config files installed by keystone
# we already generate them w/ oslo-config-generator-%{pyver}
rm -rf %{buildroot}/%{_prefix}%{_sysconfdir}

# docs generation requires everything to be installed first
%if 0%{?with_doc}
sphinx-build-%{pyver} -b html doc/source doc/build/html

sphinx-build-%{pyver} -b man doc/source doc/build/man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif
%if 0%{?with_doc}
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{pyver_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{pyver_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{service} --all-name

%pre
# 163:163 for keystone (openstack-keystone) - rhbz#752842
getent group keystone >/dev/null || groupadd -r --gid 163 keystone
getent passwd keystone >/dev/null || \
useradd --uid 163 -r -g keystone -d %{_sharedstatedir}/keystone -s /sbin/nologin \
-c "OpenStack Keystone Daemons" keystone
exit 0

%post
%sysctl_apply openstack-keystone.conf
# Install keystone.log file before, so both keystone & root users can write in it.
touch %{_localstatedir}/log/keystone/keystone.log
chown root:keystone %{_localstatedir}/log/keystone/keystone.log
chmod 660 %{_localstatedir}/log/keystone/keystone.log

%files
%license LICENSE
%doc README.rst
%if 0%{?with_doc}
%{_mandir}/man1/keystone*.1.gz
%endif
%{_bindir}/keystone-wsgi-admin
%{_bindir}/keystone-wsgi-public
%{_bindir}/keystone-manage
%{_bindir}/openstack-keystone-sample-data
%dir %{_datadir}/keystone
%attr(0644, root, keystone) %{_datadir}/keystone/keystone-dist.conf
%attr(0644, root, keystone) %{_datadir}/keystone/policy.v3cloudsample.json
%attr(0644, root, keystone) %{_datadir}/keystone/%{service}-schema.yaml
%attr(0644, root, keystone) %{_datadir}/keystone/%{service}-schema.json
%attr(0755, root, root) %{_datadir}/keystone/sample_data.sh
%attr(0644, root, keystone) %{_datadir}/keystone/wsgi-keystone.conf
%dir %attr(0750, root, keystone) %{_sysconfdir}/keystone
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/keystone.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/keystone-paste.ini
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/logging.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/policy.json
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/default_catalog.templates
%config(noreplace) %attr(0640, keystone, keystone) %{_sysconfdir}/keystone/sso_callback_template.html
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-keystone
%dir %attr(-, keystone, keystone) %{_sharedstatedir}/keystone
%dir %attr(0750, keystone, keystone) %{_localstatedir}/log/keystone
%ghost %attr(0660, root, keystone) %{_localstatedir}/log/keystone/keystone.log
%{_prefix}/lib/sysctl.d/openstack-keystone.conf


%files -n python%{pyver}-keystone -f %{service}.lang
%defattr(-,root,root,-)
%license LICENSE
%{pyver_sitelib}/keystone
%{pyver_sitelib}/keystone-*.egg-info
%exclude %{pyver_sitelib}/%{service}/tests

%files -n python%{pyver}-%{service}-tests
%license LICENSE
%{pyver_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog

