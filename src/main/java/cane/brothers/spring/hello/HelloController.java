package cane.brothers.spring.hello;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

@RestController
@RequiredArgsConstructor
@RequestMapping(value = "/api/hello", produces = {"application/json"})
class HelloController {

    @Value("${app.username}")
    String username;

    @GetMapping("/secrets")
    public ResponseEntity<String> getSecrets() {
        return ResponseEntity.of(Optional.of(username));
    }

    @GetMapping("/params")
    public ResponseEntity<String> getParams(@Value("${app.roles.whitelist}") String whitelistRole) {
        return ResponseEntity.of(Optional.of(whitelistRole));
    }
}
