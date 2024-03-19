resource "aws_network_interface" "wp_internet" {
    subnet_id   = aws_subnet.public_wp.id
  
    security_groups = [aws_security_group.wordpress.id]

    tags = {
        Name = "terraform-wp-to-internet"
    }
}

resource "aws_eip_association" "wp_eip" {
    allocation_id = aws_eip.wordpress.id
    network_interface_id = aws_network_interface.wp_internet.id
}

resource "aws_network_interface" "wp_to_db" {
    subnet_id   = aws_subnet.private_wp_db.id

    security_groups = [aws_security_group.default.id]

    tags = {
        Name = "terraform-wp-to-db"
    }
}

resource "aws_network_interface" "db_from_wp" {
    subnet_id   = aws_subnet.private_wp_db.id

    security_groups = [aws_security_group.mariadb.id]

    tags = {
        Name = "terraform-db-from-wp"
    }
}

resource "aws_network_interface" "db_to_nat" {
    subnet_id   = aws_subnet.private_db_nat.id

    security_groups = [aws_security_group.default.id]

    tags = {
        Name = "terraform-db-to-nat"
    }
}
