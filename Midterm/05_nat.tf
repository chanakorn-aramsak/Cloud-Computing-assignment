resource "aws_nat_gateway" "main" {
    allocation_id = aws_eip.nat.id
    subnet_id     = aws_subnet.public_nat.id

    tags = {
        Name = "terraform-nat"
    }
}