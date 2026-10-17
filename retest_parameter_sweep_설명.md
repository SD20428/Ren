# 평가용 데이터 열 설명

CSV: retest_parameter_sweep_sum180.csv — 32,761행, 22열.

## 남긴 항목

- prevalence_percent: 검사 전 위암 확률(%). 1.0으로 고정.
- sample_size: 표본 인원(100,000명).
- sensitivity1_percent / specificity1_percent: 1차 민감도 / 특이도(%).
- sensitivity2_percent / specificity2_percent: 2차 민감도 / 특이도(%).
- first_tp / first_tn / first_fp / first_fn: 1차 검사 TP / TN / FP / FN.
- positive_only_TP / TN / FP / FN: 1차 양성자만 재검사했을 때 최종 결과.
- negative_only_TP / TN / FP / FN: 1차 음성자만 재검사했을 때 최종 결과.
- all_TP / TN / FP / FN: 모두 재검사했을 때 최종 결과.

위 접미어는 각각 전체 열 이름에 붙는다. 예: positive_only_TN.
TP=진양성, TN=진음성, FP=위양성, FN=위음성. 모두 예상 인원이다.

## 계산 조건

1차와 2차 각각 민감도는 81~99%, 0.1%p 간격이며 특이도=180−민감도다. 각 검사의 민감도+특이도는 정확히 180%p. 두 검사의 성능 조합은 각각 독립적으로 순회한다.
재검사자는 2차 결과, 미실시자는 1차 결과를 최종 판정으로 사용한다.
질병 유무를 조건으로 검사 결과가 독립이며 검사 사이 질병 상태는 변하지 않는 교육용 모형이다. 실제 관측값이나 무작위 표본이 아니다.

## 평가 지표 계산

각 방식의 TP·TN·FP·FN으로 다음을 계산할 수 있다.

- 민감도 = TP / (TP+FN)
- 특이도 = TN / (TN+FP)
- 양성예측도(PPV) = TP / (TP+FP)
- 음성예측도(NPV) = TN / (TN+FN)
- 정확도 = (TP+TN) / (TP+TN+FP+FN)
- F1 = 2TP / (2TP+FP+FN)

백분율 표시는 계산값에 100을 곱한다. 분모가 0이면 지표는 정의되지 않는다.
검사 횟수나 비용을 평가하기 위한 열은 이번 간소화에서 제외했다.
