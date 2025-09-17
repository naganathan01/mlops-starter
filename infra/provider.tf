provider "aws" {
  region = var.region
  
  default_tags {
    tags = {
      Environment = "development"
      Project     = var.project_name
      ManagedBy   = "terraform"
    }
  }
}
