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
Version:        14.2.0
Release:        1%{?dist}
Summary:        OpenStack Identity Service
License:        ASL 2.0
URL:            http://keystone.openstack.org/
Source0:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
#

Source1:        openstack-keystone.logrotate
Source3:        openstack-keystone.sysctl
Source5:        openstack-keystone-sample-data
Source20:       keystone-dist.conf

BuildArch:      noarch
BuildRequires:  openstack-macros
BuildRequires:  python2-devel
BuildRequires:  python2-osprofiler >= 1.1.0
BuildRequires:  python2-pbr >= 2.0.0
BuildRequires:  git
# Required to build keystone.conf
BuildRequires:  python2-oslo-cache >= 1.26.0
BuildRequires:  python2-oslo-config >= 2:5.2.0
BuildRequires:  python2-passlib >= 1.6
BuildRequires:  python2-pycadf >= 2.1.0
BuildRequires:  python-redis
%if 0%{rhosp} == 0
BuildRequires:  python-zmq
%endif
# Required to compile translation files
BuildRequires:    python2-babel
# Required to build man pages
BuildRequires:  python2-oslo-policy
BuildRequires:  python2-jsonschema >= 2.6.0
BuildRequires:  python2-oslo-db >= 4.27.0
BuildRequires:  python-ldappool
BuildRequires:  python2-oauthlib
BuildRequires:  python2-pysaml2
BuildRequires:  python2-keystonemiddleware >= 4.17.0
BuildRequires:  python-webtest
BuildRequires:  python-freezegun
BuildRequires:  python2-testresources
BuildRequires:  python2-testscenarios
BuildRequires:  python-pep8
BuildRequires:  python2-oslotest

Requires:       python-keystone = %{epoch}:%{version}-%{release}
Requires:       python-keystoneclient >= 1:3.8.0

%{?systemd_requires}
BuildRequires: systemd
Requires(pre):    shadow-utils

%description
%{common_desc}

This package contains the Keystone daemon.

%package -n       python-keystone
Summary:          Keystone Python libraries

Requires:       python2-pbr >= 2.0.0
Requires:       python2-bcrypt >= 3.1.2
Requires:       python-ldap >= 3.1.0
Requires:       python-ldappool >= 2.0.0
Requires:       python-memcached >= 1.56
Requires:       python-migrate >= 0.11.0
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-paste
Requires:       python2-routes >= 2.3.1
Requires:       python2-sqlalchemy >= 1.0.10
Requires:       python-webob >= 1.7.1
Requires:       python2-passlib >= 1.7.0
Requires:       openssl
Requires:       python2-six >= 1.10.0
Requires:       python2-babel >= 2.3.4
Requires:       python2-oauthlib >= 0.6.2
Requires:       python-dogpile-cache >= 0.6.2
Requires:       python2-jsonschema >= 2.6.0
Requires:       python2-pycadf >= 2.1.0
Requires:       python2-keystonemiddleware >= 4.17.0
Requires:       python2-oslo-cache >= 1.26.0
Requires:       python2-oslo-concurrency >= 3.26.0
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-oslo-context >= 2.21.0
Requires:       python2-oslo-db >= 4.27.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-log  >= 3.38.0
Requires:       python2-oslo-messaging >= 5.29.0
Requires:       python2-oslo-middleware >= 3.31.0
Requires:       python2-oslo-policy >= 1.30.0
Requires:       python2-oslo-serialization >= 2.18.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-osprofiler >= 1.4.0
Requires:       python2-pysaml2 >= 4.5.0
Requires:       python2-stevedore >= 1.20.0
Requires:       python2-scrypt >= 0.8.0
Requires:       python2-flask >= 1.0.2
Requires:       python2-flask-restful  >= 0.3.5
Requires:       python-pytz >= 2013.6
# for Keystone Lightweight Tokens (KLWT)
Requires:       python2-cryptography >= 2.1
Requires:       python-msgpack >= 0.4.0


%description -n   python-keystone
%{common_desc}

This package contains the Keystone Python library.

%package -n python-%{service}-tests
Summary:        Keystone tests
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

# Adding python-keystone-tests-tempest as Requires to keep backward
# compatibilty
Requires:       python-keystone-tests-tempest

%description -n python-%{service}-tests
%{common_desc}

This package contains the Keystone test files.


%if 0%{?with_doc}
%package doc
Summary:        Documentation for OpenStack Identity Service

# for API autodoc
BuildRequires:  python2-sphinx >= 1.1.2
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-sphinxcontrib-apidoc
BuildRequires:  python2-flask >= 1.0.2
BuildRequires:  python2-flask-restful >= 0.3.5
BuildRequires:  python2-cryptography >= 2.1
BuildRequires:  python-dogpile-cache >= 0.5.7
BuildRequires:  python-memcached
BuildRequires:  python2-oslo-concurrency >= 3.26.0
BuildRequires:  python2-oslo-log  >= 3.38.0
BuildRequires:  python2-oslo-messaging >= 5.29.0
BuildRequires:  python2-oslo-middleware >= 3.31.0
BuildRequires:  python2-oslo-policy >= 1.30.0
BuildRequires:  python-paste-deploy
BuildRequires:  python2-routes
BuildRequires:  python-lxml
BuildRequires:  python2-mock

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
PYTHONPATH=. oslo-config-generator --config-file=config-generator/keystone.conf
PYTHONPATH=. oslo-config-generator --config-file=config-generator/keystone.conf --format yaml --output-file=%{service}-schema.yaml
PYTHONPATH=. oslo-config-generator --config-file=config-generator/keystone.conf --format json --output-file=%{service}-schema.json
# distribution defaults are located in keystone-dist.conf

%{__python2} setup.py build
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/%{service}/locale -D keystone

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

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
# we already generate them w/ oslo-config-generator
rm -rf %{buildroot}/%{_prefix}%{_sysconfdir}

# docs generation requires everything to be installed first
%if 0%{?with_doc}
sphinx-build -b html doc/source doc/build/html

sphinx-build -b man doc/source doc/build/man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif
%if 0%{?with_doc}
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{python2_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{python2_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

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


%files -n python-keystone -f %{service}.lang
%defattr(-,root,root,-)
%license LICENSE
%{python2_sitelib}/keystone
%{python2_sitelib}/keystone-*.egg-info
%exclude %{python2_sitelib}/%{service}/tests

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Mon Feb 24 2020 RDO <dev@lists.rdoproject.org> 1:14.2.0-1
- Update to 14.2.0

* Thu Apr 04 2019 RDO <dev@lists.rdoproject.org> 1:14.1.0-1
- Update to 14.1.0

* Wed Nov 21 2018 RDO <dev@lists.rdoproject.org> 1:14.0.1-2
- Use copytruncate when rotating logs and bump release

* Thu Nov 01 2018 RDO <dev@lists.rdoproject.org> 1:14.0.1-1
- Update to 14.0.1

* Wed Sep 19 2018 RDO <dev@lists.rdoproject.org> 1:14.0.0-2
- Update python2-oslo-log requirement to 3.37.0 or later

* Thu Aug 30 2018 RDO <dev@lists.rdoproject.org> 1:14.0.0-1
- Update to 14.0.0

* Fri Aug 24 2018 RDO <dev@lists.rdoproject.org> 1:14.0.0-0.2.0rc1
- Update to 14.0.0.0rc2

* Thu Aug 16 2018 RDO <dev@lists.rdoproject.org> 1:14.0.0-0.1.0rc1
- Update to 14.0.0.0rc1


