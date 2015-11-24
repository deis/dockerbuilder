package main

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
)

const usage = `
All services should provide a top-level Go program named "boot.go", compiled
to "boot". This should go in rootfs/bin/boot, and should be the entry point
for all Deis components.

An exception to this is components that may be started without a boot, or which
may be started with a simple (<20 line) shell script.
`

const prefix = "--->"

func printf(fmtStr string, args ...interface{}) {
	fmt.Printf(fmtStr+"\n", args...)
}

func errf(fmtStr string, args ...interface{}) {
	fmt.Printf("[ERROR] "+fmtStr+"\n", args...)
}

func cmdToStr(cmd *exec.Cmd) string {
	return strings.Join(cmd.Args, " ")
}

func printAndRun(cmd *exec.Cmd) {
	printf("%s %s", prefix, cmdToStr(cmd))
	out, err := cmd.CombinedOutput()
	if err != nil {
		errf("running %s [%s]", cmdToStr(cmd), err)
		os.Exit(1)
	}
	printf(string(out))
}

func main() {
	tmp := os.TempDir()
	// TODO: better perms for this dir
	if err := os.MkdirAll(tmp, os.ModePerm); err != nil {
		errf("creating temporary directory %s [%s]", tmp, err)
		os.Exit(1)
	}
	defer func() {
		if err := os.Remove(tmp); err != nil {
			errf("removing temprorary directory %s [%s]", tmp, err)
			os.Exit(1)
		}
	}()

	tarURL := os.Getenv("TAR_URL")
	if tarURL == "" {
		errf("TAR_URL environment variable not specified")
		os.Exit(1)
	}

	imgName := os.Getenv("IMG_NAME")
	if imgName == "" {
		errf("IMG_NAME environment variable not specified")
		os.Exit(1)
	}

	target := fmt.Sprintf("%s/%s", tmp, tarURL)

	// download from object storage
	cmd := exec.Command("mc", "cp", tarURL, target)
	printAndRun(cmd)

	cmd = exec.Command("tar", "xvzf", target)
	cmd.Env = os.Environ()
	cmd.Dir = tmp
	printAndRun(cmd)

	// docker build
	cmd = exec.Command("docker", "build", "-t", imgName, ".")
	cmd.Env = os.Environ()
	cmd.Dir = tmp
	printAndRun(cmd)

	// docker push
	cmd = exec.Command("docker", "push", imgName)
	cmd.Env = os.Environ()
	cmd.Dir = tmp
	printAndRun(cmd)

	// fmt.Println(usage)
}
