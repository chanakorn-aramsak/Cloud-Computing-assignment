resource "aws_eip" "nat" {
  tags = {
    Name = "terraform-nat-eip"
  }
}

resource "aws_eip" "wordpress" {
  tags = {
    Name = "terraform-wordpress-eip"
  }
}