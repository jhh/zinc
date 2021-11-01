{
  description = "Zinc zrepl console web application";

  inputs = {
    flake-utils.url = github:numtide/flake-utils;
    nixpkgs.url = github:NixOS/nixpkgs/nixos-unstable;
    poetry2nix = {
      url = github:nix-community/poetry2nix;
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };


  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    {
      # Nixpkgs overlay providing the application
      overlay = nixpkgs.lib.composeManyExtensions [
        poetry2nix.overlay
        (final: prev: {
          # The application
          zinc = prev.poetry2nix.mkPoetryApplication {
            projectDir = ./.;
          };
        })
      ];
    } // (flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlay ];
        };
      in
      rec {
        packages = {
          zinc = pkgs.zinc.dependencyEnv;
        };

        # defaultApp = apps.zinc;
        defaultPackage = packages.zinc;
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [ python3 poetry ];
          shellHook = ''
            export FLASK_APP=zinc
            export FLASK_ENV=development
          '';
        };
      }));
}
