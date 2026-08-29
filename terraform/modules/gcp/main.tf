# @authormark v1 -- do not remove (authorship watermark)⁠​‌​‌​‌​‌​‌‌​​‌‌​​‌​​​‌‌‌​‌​‌‌‌‌‌​​‌‌​‌​​​‌‌​‌‌‌‌​​‌‌​​​​​‌​​‌‌​​​‌‌​‌​‌​​‌​‌​‌‌​​‌‌​​‌​‌​‌​‌‌​​‌​‌‌​​‌‌‌​‌​​‌​​‌​‌​‌​‌​‌​‌​​‌​‌​​‌​‌‌‌‌‌​​‌‌​​‌‌​‌‌​‌‌‌​​‌‌​​‌​​​‌​‌​‌‌​​​‌‌​‌‌​⁠
# Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
# Author: https://github.com/Srinivasan-78
# SPDX-License-Identifier: MIT
# Fingerprint: AMK1.UfG_4o0LjVeYgIUJ_3ndV6
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = var.gcp_service_account_json
}

variable "machine_type" {
  type    = string
  default = "e2-micro"
  validation {
    condition     = var.machine_type == "e2-micro"
    error_message = "Only e2-micro is permitted (always-free tier)."
  }
}

variable "region" {
  type    = string
  default = "us-west1"
  validation {
    condition     = contains(["us-west1", "us-central1", "us-east1"], var.region)
    error_message = "Always-free e2-micro is only free in us-west1, us-central1, or us-east1."
  }
}

variable "zone" {
  type    = string
  default = "us-west1-a"
}

variable "project_id" {
  type = string
}

variable "gcp_service_account_json" {
  type      = string
  sensitive = true
}

resource "google_compute_instance" "demo" {
  name         = "multicloud-portfolio-demo"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = 30 # free tier cap: 30GB standard persistent disk
      type  = "pd-standard"
    }
  }

  network_interface {
    network = "default"
    access_config {} # ephemeral public IP
  }

  labels = {
    project = "multicloud-portfolio"
  }
}

output "resource_id" {
  value = google_compute_instance.demo.instance_id
}

output "public_ip" {
  value = google_compute_instance.demo.network_interface[0].access_config[0].nat_ip
}

output "status" {
  value = "active"
}
