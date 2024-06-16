data "local_file" "ssh_public_key" {
  filename = "./ssh/key.pub"
}

resource "proxmox_virtual_environment_vm" "train_env" {
  name      = "train-env"
  node_name = var.node3_id

  initialization {

    ip_config {
      ipv4 {
        address = "10.10.10.100/24"
        gateway = "10.10.10.1"
      }
    }

    user_account {
      username = "debian"
      keys     = [trimspace(data.local_file.ssh_public_key.content)]
    }
  }

  cpu {
    cores = 28
  }

  memory {
    dedicated = 30000
  }

  disk {
    datastore_id = "local-lvm"
    file_id      = proxmox_virtual_environment_download_file.debian_cloud_image3.id
    interface    = "virtio0"
    iothread     = true
    discard      = "on"
    size         = 50
  }

  network_device {
    bridge = "vmbr0"
  }
}

resource "proxmox_virtual_environment_vm" "train_env2" {
  name      = "train-env2"
  node_name = var.node2_id

  initialization {

    ip_config {
      ipv4 {
        address = "10.10.10.101/24"
        gateway = "10.10.10.1"
      }
    }

    user_account {
      username = "debian"
      keys     = [trimspace(data.local_file.ssh_public_key.content)]
    }
  }

  cpu {
    cores = 28
  }

  memory {
    dedicated = 30000
  }

  disk {
    datastore_id = "local-lvm"
    file_id      = proxmox_virtual_environment_download_file.debian_cloud_image2.id
    interface    = "virtio0"
    iothread     = true
    discard      = "on"
    size         = 50
  }

  network_device {
    bridge = "vmbr0"
  }
}

resource "proxmox_virtual_environment_vm" "train_env3" {
  name      = "train-env3"
  node_name = var.node1_id

  initialization {

    ip_config {
      ipv4 {
        address = "10.10.10.102/24"
        gateway = "10.10.10.1"
      }
    }

    user_account {
      username = "debian"
      keys     = [trimspace(data.local_file.ssh_public_key.content)]
    }
  }

  cpu {
    cores = 12
  }

  memory {
    dedicated = 16000
  }

  disk {
    datastore_id = "local-lvm"
    file_id      = proxmox_virtual_environment_download_file.debian_cloud_image1.id
    interface    = "virtio0"
    iothread     = true
    discard      = "on"
    size         = 50
  }

  network_device {
    bridge = "vmbr0"
  }
}

resource "proxmox_virtual_environment_download_file" "debian_cloud_image1" {
  content_type       = "iso"
  datastore_id       = "local"
  file_name          = "debian-12-generic-amd64-20231228-1609.img"
  node_name          = var.node1_id
  url                = "https://cloud.debian.org/images/cloud/bookworm/20231228-1609/debian-12-generic-amd64-20231228-1609.qcow2"
  checksum           = "d2fbcf11fb28795842e91364d8c7b69f1870db09ff299eb94e4fbbfa510eb78d141e74c1f4bf6dfa0b7e33d0c3b66e6751886feadb4e9916f778bab1776bdf1b"
  checksum_algorithm = "sha512"
}

resource "proxmox_virtual_environment_download_file" "debian_cloud_image2" {
  content_type       = "iso"
  datastore_id       = "local"
  file_name          = "debian-12-generic-amd64-20231228-1609.img"
  node_name          = var.node2_id
  url                = "https://cloud.debian.org/images/cloud/bookworm/20231228-1609/debian-12-generic-amd64-20231228-1609.qcow2"
  checksum           = "d2fbcf11fb28795842e91364d8c7b69f1870db09ff299eb94e4fbbfa510eb78d141e74c1f4bf6dfa0b7e33d0c3b66e6751886feadb4e9916f778bab1776bdf1b"
  checksum_algorithm = "sha512"
}

resource "proxmox_virtual_environment_download_file" "debian_cloud_image3" {
  content_type       = "iso"
  datastore_id       = "local"
  file_name          = "debian-12-generic-amd64-20231228-1609.img"
  node_name          = var.node3_id
  url                = "https://cloud.debian.org/images/cloud/bookworm/20231228-1609/debian-12-generic-amd64-20231228-1609.qcow2"
  checksum           = "d2fbcf11fb28795842e91364d8c7b69f1870db09ff299eb94e4fbbfa510eb78d141e74c1f4bf6dfa0b7e33d0c3b66e6751886feadb4e9916f778bab1776bdf1b"
  checksum_algorithm = "sha512"
}
