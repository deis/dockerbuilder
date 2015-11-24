package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"strings"

	"github.com/codegangsta/cli"
)

const description = "dockerbuilder is a simple program that downloads code, runs 'docker build' and 'docker run'. It's intended (but not required) for use with the Deis builder (https://github.com/deis/builder), which launches it as a Kubernetes pod to handle Dockerfile based builds."

const runUsage = "download a gzipped tarball (*.tar.gz file) from a S3-compatible endpoint specified at $TAR_URL (environment variable) to a temporary directory, unzip it and then run 'docker build -t $IMG_NAME .' and 'docker run $IMG_NAME' on it"

const (
	prefix             = "--->"
	accessKeyEnvVar    = "ACCESS_KEY_FILE"
	accessSecretEnvVar = "ACCESS_SECRET_FILE"
)

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

// readAccessKeyAndSecret attempts to
func readAccessKeyAndSecret() ([]byte, []byte, error) {
	keyLoc := os.Getenv(accessKeyEnvVar)
	if keyLoc == "" {
		return nil, nil, fmt.Errorf("missing %s", accessKeyEnvVar)
	}

	secretLoc := os.Getenv(accessSecretEnvVar)
	if secretLoc == "" {
		return nil, nil, fmt.Errorf("missing %s", accessSecretEnvVar)
	}

	accessKey, err := ioutil.ReadFile(keyLoc)
	if err != nil {
		return nil, nil, fmt.Errorf("reading %s [%s]", keyLoc, err)
	}

	accessSecret, err := ioutil.ReadFile(secretLoc)
	if err != nil {
		return nil, nil, fmt.Errorf("reading %s [%s]", secretLoc, err)
	}
	return accessKey, accessSecret, nil
}

func main() {
	app := cli.NewApp()
	app.Name = "dockerbuilder"
	app.Usage = description

	app.Commands = []cli.Command{
		{
			Name:        "run",
			Aliases:     []string{"r"},
			Usage:       runUsage,
			Description: runUsage,
			Action:      run,
		},
	}

	app.Run(os.Args)
}

func run(c *cli.Context) {
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

	// configure key and secret
	accessKey, accessSecret, err := readAccessKeyAndSecret()
	if err != nil {
		errf("error reading access key and secret [%s]", err)
		os.Exit(1)
	}

	cmd := exec.Command("mc", "config", "host", "add", tarURL, string(accessKey), string(accessSecret))
	cmd.Env = os.Environ()
	printAndRun(cmd)

	target := fmt.Sprintf("%s/%s", tmp, tarURL)

	// download from object storage
	cmd = exec.Command("mc", "cp", tarURL, target)
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
