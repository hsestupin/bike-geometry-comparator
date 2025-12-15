{ pkgs ? import <nixpkgs> { }
,
}:
let
  projectDir = builtins.toString ./.;
  bikeBuildDir = "${projectDir}/build";
  databaseCsv = "${bikeBuildDir}/database.csv";
  frontendSrcDir = "${projectDir}/src/client";
  frontendPublicDir = "${frontendSrcDir}/public";
  build-database = pkgs.writeShellApplication {
    name = "build-database";
    text = ''
      uv run bgc
      mkdir -p ${frontendPublicDir} && cp ${databaseCsv} ${frontendPublicDir}
    '';
  };
in
pkgs.mkShell {
  packages = [
    pkgs.pnpm
    pkgs.nodejs
    pkgs.uv

    build-database
  ];
  shellHook = ''
    alias pnpm='pnpm -C ${frontendSrcDir}'
  '';
}
