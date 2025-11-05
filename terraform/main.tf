provider "aws" {
  region = "ap-south-1"
}

resource "aws_key_pair" "weather_key" {
  key_name   = "weather-key"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_security_group" "weather_sg" {
  name_prefix = "weather-sg"
  description = "Allow HTTP and SSH"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "weather_app" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.weather_key.key_name
  vpc_security_group_ids = [aws_security_group.weather_sg.id]

  tags = {
    Name = "WeatherAppServer"
  }
}

output "public_ip" {
  value = aws_instance.weather_app.public_ip
}
