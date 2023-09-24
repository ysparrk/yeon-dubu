package yeon.dubu.money.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;
import yeon.dubu.auth.enumeration.RoleType;
import yeon.dubu.couple.domain.Couple;
import yeon.dubu.couple.repository.CoupleRepository;
import yeon.dubu.money.domain.Money;
import yeon.dubu.money.dto.request.MoneyCashReqDto;
import yeon.dubu.money.dto.response.MoneyCashResDto;
import yeon.dubu.money.repository.MoneyRepository;
import yeon.dubu.user.domain.User;
import yeon.dubu.user.enumeration.UserRole;
import yeon.dubu.user.repository.UserRepository;

import java.time.LocalDate;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class MoneyServiceImplTest {

    @Autowired
    UserRepository userRepository;
    @Autowired
    CoupleRepository coupleRepository;
    @Autowired
    MoneyRepository moneyRepository;
    @Autowired
    MoneyService moneyService;

    static User USER1;
    static User USER2;

    @BeforeEach
    void beforeEach() {
        Couple couple = Couple.builder()
                .weddingDate(LocalDate.of(2024, 05, 25))
                .build();

        Couple createCouple = coupleRepository.save(couple);

        User user1 = User.builder()
                .name("예비신부")
                .couple(createCouple)
                .userRole(UserRole.BRIDE)
                .roleType(RoleType.USER)
                .build();

        USER1 = userRepository.save(user1);

        User user2 = User.builder()
                .name("예비신랑")
                .couple(createCouple)
                .userRole(UserRole.GROOM)
                .roleType(RoleType.USER)
                .build();

        USER2 = userRepository.save(user2);

        // TODO: couple 생성 후 money 생기는 로직 작성 후 삭제필요
        Money money = Money.builder()
                .totalCash(0L)
                .totalAccount(0L)
                .expectExpenditure(0L)
                .completeExpenditure(0L)
                .user(USER1)
                .build();

        moneyRepository.save(money);

        Money money2 = Money.builder()
                .totalCash(0L)
                .totalAccount(0L)
                .expectExpenditure(0L)
                .completeExpenditure(0L)
                .user(USER2)
                .build();

        moneyRepository.save(money2);

    }

    @DisplayName("사용자 현금 등록")
    @Transactional
    @Test
    void insertCash() {
        // given
        MoneyCashReqDto moneyCashReqDto = MoneyCashReqDto.builder()
                .totalCash(1000000L)
                .build();

        // when
        Money insertedCash = moneyService.insertCash(moneyCashReqDto, USER1.getId());

        // then
        assertThat(moneyRepository.findByUser(USER1).get().getTotalCash()).isEqualTo(insertedCash.getTotalCash());
    }
    @DisplayName("couple의 현금 조회")
    @Test
    @Transactional
    void searchTotalCash() {
        // given
        MoneyCashReqDto moneyCash1 = MoneyCashReqDto.builder()
                .totalCash(1000000L)
                .build();

        MoneyCashReqDto moneyCash2 = MoneyCashReqDto.builder()
                .totalCash(2000000L)
                .build();

        moneyService.insertCash(moneyCash1, USER1.getId());
        moneyService.insertCash(moneyCash2, USER2.getId());

        // when
        MoneyCashResDto totalCash = moneyService.searchTotalCash(USER2.getId());

        // then
        Long actualCash = totalCash.getBrideTotalCash() + totalCash.getGroomTotalCash();
        assertThat(actualCash).isEqualTo(3000000L);

    }
}