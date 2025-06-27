package cane.brothers.spring.hello;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

@Slf4j
@RestController
@RequiredArgsConstructor
@RequestMapping(value = "/api/hello/secrets", produces = {"application/json"})
public class HelloController {

    @Value("${app.username}")
    String username;

    @GetMapping()
    public ResponseEntity<String> getSecrets() {
        return ResponseEntity.of(Optional.of(username));
    }
}
