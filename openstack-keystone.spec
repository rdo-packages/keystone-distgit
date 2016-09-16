%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global service keystone

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-keystone
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:          1
Version:        XXX
Release:        XXX
Summary:        OpenStack Identity Service
License:        ASL 2.0
URL:            http://keystone.openstack.org/
Source0:        http://tarballs.openstack.org/%{service}/%{service}-master.tar.gz
Source1:        openstack-keystone.logrotate
Source3:        openstack-keystone.sysctl
Source5:        openstack-keystone-sample-data
Source20:       keystone-dist.conf

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-osprofiler >= 1.1.0
BuildRequires:  python-pbr >= 1.8
# Required to build keystone.conf
BuildRequires:  python-oslo-cache >= 1.5.0
BuildRequires:  python-oslo-config >= 2:3.9.0
BuildRequires:  python-passlib >= 1.6
BuildRequires:  python-pycadf >= 2.1.0
BuildRequires:  python-redis
BuildRequires:  python-zmq
# Required to compile translation files
BuildRequires:    python-babel
# Required to build man pages
BuildRequires:  python-oslo-sphinx >= 2.5.0
BuildRequires:  python-sphinx >= 1.1.2

Requires:       python-keystone = %{epoch}:%{version}-%{release}
Requires:       python-keystoneclient >= 1:2.3.1

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
Requires(pre):    shadow-utils

%description
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains the Keystone daemon.

%package -n       python-keystone
Summary:          Keystone Python libraries

Requires:       python-pbr
Requires:       python-ldap
Requires:       python-ldappool
Requires:       python-memcached
Requires:       python-migrate >= 0.9.6
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-paste
Requires:       python-routes >= 1.12.3
Requires:       python-sqlalchemy >= 1.0.10
Requires:       python-webob >= 1.2.3
Requires:       python-passlib >= 1.6
Requires:       PyPAM
Requires:       python-iso8601
Requires:       openssl
Requires:       python-netaddr
Requires:       python-six >= 1.9.0
Requires:       python-babel >= 2.3.4
Requires:       python-oauthlib >= 0.6
Requires:       python-dogpile-cache >= 0.6.2
Requires:       python-jsonschema
Requires:       python-pycadf >= 2.1.0
Requires:       python-posix_ipc
Requires:       python-keystonemiddleware >= 4.3.0
Requires:       python-oslo-cache >= 1.5.0
Requires:       python-oslo-concurrency >= 3.8.0
Requires:       python-oslo-config >= 2:3.14.0
Requires:       python-oslo-context >= 2.9.0
Requires:       python-oslo-db >= 4.10.0
Requires:       python-oslo-i18n >= 3.4.0
Requires:       python-oslo-log >= 3.2.0
Requires:       python-oslo-messaging >= 5.2.0
Requires:       python-oslo-middleware >= 3.7.0
Requires:       python-oslo-policy >= 1.9.0
Requires:       python-oslo-serialization >= 2.4.0
Requires:       python-oslo-utils >= 3.16.0
Requires:       python-osprofiler >= 1.4.0
Requires:       python-pysaml2 >= 2.4.0
Requires:       python-stevedore >= 1.16.0
# for Keystone Lightweight Tokens (KLWT)
Requires:       python-cryptography
Requires:       python-msgpack


%description -n   python-keystone
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains the Keystone Python library.

%package -n python-%{service}-tests
Summary:        Keystone tests
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

%description -n python-%{service}-tests
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains the Keystone test files.


%if 0%{?with_doc}
%package doc
Summary:        Documentation for OpenStack Identity Service

# for API autodoc
BuildRequires:  python-cryptography
BuildRequires:  python-dogpile-cache >= 0.5.7
BuildRequires:  python-jsonschema
BuildRequires:  python-keystonemiddleware >= 4.3.0
BuildRequires:  python-ldappool
BuildRequires:  python-memcached
BuildRequires:  python-oauthlib
BuildRequires:  python-oslo-concurrency >= 3.6.0
BuildRequires:  python-oslo-db >= 4.6.0
BuildRequires:  python-oslo-log >= 3.2.0
BuildRequires:  python-oslo-messaging >= 4.5.0
BuildRequires:  python-oslo-middleware >= 3.7.0
BuildRequires:  python-oslo-policy >= 0.5.0
BuildRequires:  python-paste-deploy
BuildRequires:  python-pysaml2
BuildRequires:  python-routes

%description doc
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains documentation for Keystone.
%endif

%prep
%setup -q -n keystone-%{upstream_version}

find . \( -name .gitignore -o -name .placeholder \) -delete
find keystone -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

# adjust paths to WSGI scripts
sed -i 's#/local/bin#/bin#' httpd/wsgi-keystone.conf
sed -i 's#apache2#httpd#' httpd/wsgi-keystone.conf

%build
PYTHONPATH=. oslo-config-generator --config-file=config-generator/keystone.conf
# distribution defaults are located in keystone-dist.conf

%{__python2} setup.py build
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/%{service}/locale

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

install -d -m 755 %{buildroot}%{_sysconfdir}/keystone
install -p -D -m 640 etc/keystone.conf.sample %{buildroot}%{_sysconfdir}/keystone/keystone.conf
install -p -D -m 640 etc/keystone-paste.ini %{buildroot}%{_sysconfdir}/keystone/keystone-paste.ini
install -p -D -m 644 %{SOURCE20} %{buildroot}%{_datadir}/keystone/keystone-dist.conf
install -p -D -m 644 etc/policy.v3cloudsample.json %{buildroot}%{_datadir}/keystone/policy.v3cloudsample.json
install -p -D -m 640 etc/logging.conf.sample %{buildroot}%{_sysconfdir}/keystone/logging.conf
install -p -D -m 640 etc/default_catalog.templates %{buildroot}%{_sysconfdir}/keystone/default_catalog.templates
install -p -D -m 640 etc/policy.json %{buildroot}%{_sysconfdir}/keystone/policy.json
install -p -D -m 640 etc/sso_callback_template.html %{buildroot}%{_sysconfdir}/keystone/sso_callback_template.html
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-keystone
install -d -m 755 %{buildroot}%{_prefix}/lib/sysctl.d
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_prefix}/lib/sysctl.d/openstack-keystone.conf
# Install sample data script.
install -p -D -m 755 tools/sample_data.sh %{buildroot}%{_datadir}/keystone/sample_data.sh
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_bindir}/openstack-keystone-sample-data
# Install sample HTTPD integration files
install -p -D -m 644 httpd/keystone.py  %{buildroot}%{_datadir}/keystone/keystone.wsgi
install -p -D -m 644 httpd/wsgi-keystone.conf  %{buildroot}%{_datadir}/keystone/

install -d -m 755 %{buildroot}%{_sharedstatedir}/keystone
install -d -m 755 %{buildroot}%{_localstatedir}/log/keystone

# cleanup config files installed by keystone
# we already generate them w/ oslo-config-generator
rm -rf %{buildroot}/%{_prefix}%{_sysconfdir}

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
%if 0%{?with_doc}
make html
%endif
make man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/
popd
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
%{_mandir}/man1/keystone*.1.gz
%{_bindir}/keystone-wsgi-admin
%{_bindir}/keystone-wsgi-public
%{_bindir}/keystone-manage
%{_bindir}/openstack-keystone-sample-data
%dir %{_datadir}/keystone
%attr(0644, root, keystone) %{_datadir}/keystone/keystone-dist.conf
%attr(0644, root, keystone) %{_datadir}/keystone/policy.v3cloudsample.json
%attr(0755, root, root) %{_datadir}/keystone/sample_data.sh
%attr(0644, root, keystone) %{_datadir}/keystone/keystone.wsgi
%attr(0644, root, keystone) %{_datadir}/keystone/wsgi-keystone.conf
%dir %attr(0750, root, keystone) %{_sysconfdir}/keystone
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/keystone.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/keystone-paste.ini
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/logging.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/default_catalog.templates
%config(noreplace) %attr(0640, keystone, keystone) %{_sysconfdir}/keystone/policy.json
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
%exclude %{python2_sitelib}/keystone_tempest_plugin

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests
%{python2_sitelib}/keystone_tempest_plugin

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
