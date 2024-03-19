resource "aws_route_table" "public" {
    vpc_id = aws_vpc.main.id

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.main.id
    }

    tags = {
        Name = "terraform-rt-public"
    }
}

resource "aws_route_table_association" "public_wp" {
    subnet_id = aws_subnet.public_wp.id
    route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_nat" {
    subnet_id = aws_subnet.public_nat.id
    route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
    vpc_id = aws_vpc.main.id

    tags = {
        Name = "terraform-rt-private"
    }
}

resource "aws_route_table_association" "private_wp_db" {
    subnet_id = aws_subnet.private_wp_db.id
    route_table_id = aws_route_table.private.id
}

resource "aws_route_table" "private_with_nat" {
    vpc_id = aws_vpc.main.id

    route {
        cidr_block = "0.0.0.0/0"
        nat_gateway_id = aws_nat_gateway.main.id
    }

    tags = {
        Name = "terraform-private-with-nat"
    }
}

resource "aws_route_table_association" "private_db_nat" {
    subnet_id = aws_subnet.private_db_nat.id
    route_table_id = aws_route_table.private_with_nat.id
}
