resource "aws_subnet" "public_wp" {
    vpc_id            = aws_vpc.main.id
    cidr_block        = "10.0.0.16/28" # BEGIN: public_wp_cidr_block
    availability_zone = var.availability_zone

    tags = {
        Name = "terraform-public-wp"
    }
}

resource "aws_subnet" "public_nat" {
    vpc_id            = aws_vpc.main.id
    cidr_block        = "10.0.0.32/28" # BEGIN: public_nat_cidr_block
    availability_zone = var.availability_zone

    tags = {
        Name = "terraform-public-nat"
    }
}

resource "aws_subnet" "private_wp_db" {
    vpc_id            = aws_vpc.main.id
    cidr_block        = "10.0.0.48/28" # BEGIN: private_wp_db_cidr_block
    availability_zone = var.availability_zone

    tags = {
        Name = "terraform-private-wp-db"
    }
}

resource "aws_subnet" "private_db_nat" {
    vpc_id            = aws_vpc.main.id
    cidr_block        = "10.0.0.0/28" # BEGIN: private_db_nat_cidr_block
    availability_zone = var.availability_zone

    tags = {
        Name = "terraform-private-db-nat"
    }
}