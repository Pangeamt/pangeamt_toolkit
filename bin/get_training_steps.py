#!/usr/bin/env python

import torch
import sys


def main(path):
    model = torch.load(path)
    print(model["optim"]["training_step"])


if __name__ == "__main__":
    main(sys.argv[1])
