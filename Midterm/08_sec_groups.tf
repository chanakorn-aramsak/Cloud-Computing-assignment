resource "aws_security_group" "default" {
    name        = "default-sg-tf"
    description = "Allow all traffic in VPC"
    vpc_id      = aws_vpc.main.id
    
    ingress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "terraform-default-sg"
    }
}

resource "aws_security_group" "wordpress" {
    name        = "wordpress-sg"
    description = "Allow traffic to WordPress server"
    vpc_id      = aws_vpc.main.id

    ingress {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 443
        to_port = 443
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = -1
        to_port = -1
        protocol = "icmp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "terraform-wp-server-sg"
    }
}

resource "aws_security_group" "mariadb" {
    name        = "mariadb-sg"
    description = "Allow inbound traffic to database server only from WordPress server"
    vpc_id      = aws_vpc.main.id
    
    ingress {
        from_port   = 3306
        to_port     = 3306
        protocol    = "tcp"
        security_groups = [aws_security_group.wordpress.id]
    }

    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        security_groups = [aws_security_group.wordpress.id]
    }

    ingress {
        from_port = -1
        to_port = -1
        protocol = "icmp"
        security_groups = [aws_security_group.wordpress.id]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "terraform-mariadb-sg"
    }
}
