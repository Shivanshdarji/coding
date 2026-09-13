import javafx.application.Application; import javafx.scene.Scene;
import javafx.scene.control.Label; import javafx.scene.control.Button;
import javafx.scene.control.ToggleGroup; import javafx.scene.layout.VBox;
import javafx.scene.layout.Pane;
import javafx.scene.control.RadioButton; import javafx.stage.Stage;
public class ButtonFX extends Application{ public static void main(String[] ar){launch(ar);
}
public void start(Stage stage){ VBox v = new VBox();
Label l = new Label("Darji Shivansh"); Pane pane = new Pane(l);
ToggleGroup tg = new ToggleGroup(); RadioButton red = new RadioButton("Red"); RadioButton blue = new RadioButton("Blue"); RadioButton green = new RadioButton("Green"); red.setToggleGroup(tg); green.setToggleGroup(tg); blue.setToggleGroup(tg);
tg.selectedToggleProperty().addListener((obs, oldVal, newVal) ->{ if(((RadioButton)newVal).getText() == "Red"){
l.setStyle("-fx-text-fill: red;");
}else if(((RadioButton)newVal).getText() == "Blue"){ l.setStyle("-fx-text-fill: blue;");
}else if(((RadioButton)newVal).getText() == "Green"){ l.setStyle("-fx-text-fill: green;");
}
});
Button b1 = new Button("Left"); Button b2 = new Button("Right"); b2.setLayoutX(50);
v.getChildren().addAll(pane,red,blue,green,b1,b2); b2.setOnAction(event -> { if(250>=(l.getLayoutX()+50)){ l.setLayoutX(l.getLayoutX()+50);
}
});
b1.setOnAction(event -> { if(0<=(l.getLayoutX()-50)){ l.setLayoutX(l.getLayoutX()-50);
}
});
Scene scene = new Scene(v,300,250); stage.setTitle("Application_08"); stage.setScene(scene);
stage.show();
}
     }
