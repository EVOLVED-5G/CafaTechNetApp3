resource "kubernetes_pod" "CafaTechNetApp2" {
  metadata {
    name = "CafaTechNetApp2"
    namespace = "evolved5g"
    labels = {
      app = "CafaTechNetApp2_app"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/dummy-netapp:latest"
      name  = "dummy-netapp"
    }
  }
}

resource "kubernetes_service" "CafaTechNetApp2_service" {
  metadata {
    name = "CafaTechNetApp_service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.CafaTechNetApp2.metadata.0.labels.app
    }
    port {
      port = 1191
      target_port = 1191
    }
  }
}
