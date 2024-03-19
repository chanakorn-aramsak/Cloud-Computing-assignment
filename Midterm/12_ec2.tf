resource "aws_instance" "db" {
    ami = var.ami
    instance_type = "t2.micro"
    availability_zone = var.availability_zone
    
    network_interface {
        device_index = 0
        network_interface_id = aws_network_interface.db_to_nat.id
    }

    user_data = templatefile("init-mariadb.tftpl", {
    database_name = var.database_name,
    database_user = var.database_user,
    database_pass = var.database_pass
  })
    tags = {
        Name = "terraform-db"
    }

}

resource "aws_network_interface_attachment" "db_from_wp" {
    device_index = 1
    instance_id = aws_instance.db.id
    network_interface_id = aws_network_interface.db_from_wp.id
}

resource "aws_instance" "wp_server" {
    depends_on = [ aws_instance.db, aws_network_interface_attachment.db_from_wp, aws_iam_access_key.s3_user ]

    ami = var.ami
    instance_type = "t2.micro"
    availability_zone = var.availability_zone

    network_interface {
        device_index = 0
        network_interface_id = aws_network_interface.wp_internet.id
    }

    user_data = templatefile("init-wordpress.tftpl", {
        db_host = aws_instance.db.private_ip,
        db_name = var.database_name,
        db_user = var.database_user,
        db_pass = var.database_pass,
        wp_public_ip = aws_eip.wordpress.public_ip,
        wp_title = "My WordPress Blog",
        admin_user = var.admin_user,
        admin_pass = var.admin_pass,
        access_key = aws_iam_access_key.s3_user.id,
        secret_key = aws_iam_access_key.s3_user.secret,
        bucket_name = var.bucket_name,
        region = var.region
        })

    tags = {
        Name = "terraform-wordpress"
    }
}

resource "aws_network_interface_attachment" "wp_to_db" {
    device_index = 1
    instance_id = aws_instance.wp_server.id
    network_interface_id = aws_network_interface.wp_to_db.id
}