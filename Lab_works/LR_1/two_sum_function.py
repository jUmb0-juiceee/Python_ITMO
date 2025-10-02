def two_sum(nums, target):
    if nums != [int(i) for i in nums]:
        return 'ERROR (тип данных)'
    for _o1 in range(len(nums) - 1):
        for _o2 in range(_o1 + 1, len(nums)):
            if nums[_o1] + nums[_o2] == target:
                res = [_o1, _o2]
                return res
    else:
        return None
