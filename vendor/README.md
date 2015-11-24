# Vendor

All Deis projects use the Go 1.5+ Vendoring solution.

For Go 1.5, environments should be set to `GO15VENDOREXPERIMENT=1`.

All dependencies for the present project should be referenced via the
`vendor/` directory, and we should not require developers to store
dependencies directly in their `$GOPATH`.

Tools like `godep` and `glide` can be used for downloading fixed
dependencies into the `vendor/` directory.
