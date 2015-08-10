# Copyright 2015 CloudRouter Project Authors.
BASE_NAME			:= fedora
BASE_DISPLAY_NAME	:= Fedora
PKG_NAME			:= cloudrouter-$(BASE_NAME)-release
RPM_NAME			:= $(PKG_NAME)
VERSION				:= 2
SRC_FILE			:= $(PKG_NAME)-$(VERSION).tar.gz

# mksrc RPM_NAME SRC_FILE dist
mksrc = rm -rf $(1)-$(VERSION); \
	mkdir -p $(1)-$(VERSION); \
	find $(PKG_NAME) -maxdepth 1 -type f -exec cp {} $(1)-$(VERSION)/. \;; \
	find $(PKG_NAME)/repo -maxdepth 1 -type f -exec cp {} $(1)-$(VERSION)/. \;; \
	cp LICENSE README.md $(1)-$(VERSION)/.; \
	tar cvf $(2) $(1)-$(VERSION)

rpmbuild = rpmbuild --define "_topdir %(pwd)/rpm-build" \
	    --define "_builddir %{_topdir}" \
	    --define "_rpmdir %{_topdir}" \
	    --define "_srcrpmdir %{_topdir}" \
	    --define '_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm' \
	    --define "_specdir %{_topdir}" \
	    --define "_sourcedir  %{_topdir}" \
	    --define "distribution  $(1)" \
	    -ba $(PKG_NAME).spec

all: rpm

$(SRC_FILE):
	$(call mksrc,$(RPM_NAME),$(SRC_FILE))

# Phony targets for cleanup and similar uses
#
 .PHONY: clean

source: $(SRC_FILE)

rpm: $(SRC_FILE)
	mkdir -p rpm-build
	cp $(SRC_FILE) rpm-build
	$(call rpmbuild,$(BASE_NAME))

clean:
	rm -f $(SRC_FILE)
	rm -rf $(RPM_NAME)-$(VERSION)
	rm -rf rpm-build
