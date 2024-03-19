variable "region" {
    type = string
    description = "Deployment AWS Region"
}

variable "availability_zone" {
    type = string
    description = "Deployment AWS Availability Zone"
}

variable "ami" {
    type = string
    description = "AMI for EC2 instances"
}

variable "bucket_name" {
    type = string
    description = "S3 bucket for Wordpress"
}

variable "database_name" {
    type = string
    description = "Wordpress DB name"
}

variable "database_user" {
    type = string
    description = "Wordpress DB user"
}

variable "database_pass" {
    type = string
    description = "Wordpress DB password"
}

variable "admin_user" {
    type = string
    description = "Wordpress admin username"
}

variable "admin_pass" {
    type = string
    description = "Wordpress admin password"
}