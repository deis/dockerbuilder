package main

import (
	"fmt"
	"log"
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

func cmdToStr(cmd *exec.Command) string {
	return strings.Join(cmd.Args)
}

func main() {
	tmp := os.TempDir()
	// TODO: better perms for this dir
	if err := os.MkdirAll(tmp, os.ModePerm); err != nil {
		log.Printf("[ERROR] creating temporary directory %s [%s]", tmp, err)
		os.Exit(1)
	}
	defer func() {
		if err := os.Remove(tmp); err != nil {
			log.Printf("[ERROR] removing temporary directory %s [%s]", tmp, err)
			os.Exit(1)
		}
	}()

	tarURL := os.Getenv("TAR_URL")
	if tarURL == "" {
		log.Println("[ERROR] TAR_URL not specified")
		os.Exit(1)
	}

	imgName := os.Getenv("IMG_NAME")
	if imgName == "" {
		log.Println("[ERROR] IMG_NAME (docker image name) not specified")
		os.Exit(1)
	}

	target := fmt.Sprintf("%s/%s", tmp, tarURL)

	// download from object storage
	cmd := exec.Command("mc", "cp", tarURL, target)
	out, err := cmd.CombinedOutput()
	if err != nil {
		log.Printf("[ERROR] downloading from %s [%s]", tarURL, err)
		os.Exit(1)
	}

	// docker build
	cmd := exec.Command("docker", "build", "-t", imgName, ".")
	cmd.Env = os.Environ()
	cmd.Dir = tmp

	out, err = cmd.CombinedOutput()
	if err != nil {
		log.Printf("[ERROR] running %s [%s]", cmdToStr(cmd), err)
		os.Exit(1)
	}

	// docker push
	cmd := exec.Command("docker", "push", imgName)
	cmd.Env = os.Environ()
	cmd.Dir = tmp
	out, err = cmd.CombinedOutput()
	if err != nil {
		log.Printf("[ERROR] running %s [%s]", cmdToStr(cmd), err)
		os.Exit(1)
	}

	fmt.Println(usage)
}
